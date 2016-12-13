import os, sys, glob, mahotas, pickle
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
from sklearn import svm
from skimage.feature import greycomatrix
from scipy.ndimage import morphology
from scipy.stats import skew, boxcox
from operator import add
clf = None


def call_haralick0(subimage):
    ''' Caluculate Haralick texture features from a square subimage
        Always return 4 x 13 matrix either with values for each angle or with NaN.
        The is used for easy pickling (needed for multiprocessing)
        Parameters
        ----------
        subimage : ndarray
        2D array with data in UINT8
        Returns
        -------
        haralick : ndarray
        4 x 13 matrix with Haralick texture features or NaN
        '''
    try:
        haralick = mahotas.features.haralick(subimage, True)
    except ValueError:
        haralick = np.zeros((4, 13)) + np.nan
    if haralick.shape != (4, 13):  haralick = np.zeros((4, 13)) + np.nan

    return haralick


def call_haralick1(subimage):
    ''' Caluculate Haralick texture features from a square subimage
        
        Always return 4 x 13 matrix either with values for each angle or with NaN.
        The is used for easy pickling (needed for multiprocessing)
        
        Parameters
        ----------
        subimage : ndarray
        2D array with data in UINT8
        Returns
        -------
        haralick : ndarray
        4 x 13 matrix with Haralick texture features or NaN
        '''
    cooccuranceDistances = range(1,np.min(subimage.shape)//2)
    haralick = np.zeros((4,13))
    for iDist in cooccuranceDistances:
        try:
            haralick = mahotas.features.haralick(
                           subimage, ignore_zeros=True, distance=iDist )
        except ValueError:
            haralick = np.zeros((4, 13)) + np.nan
        if haralick.shape != (4, 13):  haralick = np.zeros((4, 13)) + np.nan
    haralick /= len(cooccuranceDistances)

    return haralick


# GLCM computation result from MAHOTAS is different from that of SCIKIT-IMAGE.
# MAHOTAS considers distance as number of cells in given direction.
# SCKIT-IMAGE considers distance as euclidian distance, and take values form
# the nearest neighbor when the euclidian distance is not integer.
# e.g.) reference cell coordinate (100,100), direction = 45 deg., distance = 3
# MAHOTAS counts co-occurence pair between (100,100) and (103,103).
# SCIKIT-IMAGE counts co-occurence pair between (100,100) and (102,102), because
# a euclidian distance of 3 in direction of 45 degree corresponds to 3/sqrt(2),
# which is 2.121 along x and y coordinate, and 2.12 is closer to 2 rather than 3.


def call_haralick2(subimage):
    
    # FOR COMPUTING GLCM,
    # USE SCIKIT-IMAGE PACKAGE WHICH CAN HANDLE MULTIPLE CO-OCCURANCE DISTANCE.
    # FOR AVERAGNIG TEXTURE FEATURES FROM MULTIPLE DISTANCES, TAKE MEAN AT FEATURE LEVEL
    
    cooccuranceDistances = range(1,np.min(subimage.shape)//2)
    directions = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcmDim = int(np.max(subimage)+1)
    glcm = greycomatrix( subimage, distances=cooccuranceDistances, \
                         angles=directions, levels=glcmDim, \
                         symmetric=True, normed=True )
    haralick = np.zeros((len(cooccuranceDistances),4,13))
    for distIdx in range(glcm.shape[2]):
        glcm_subset = np.swapaxes(glcm[:,:,distIdx,:].T,1,2)
        try:
            tmp_haralick = \
                mahotas.features.texture.haralick_features(glcm_subset, ignore_zeros=True)
        except ValueError:
            tmp_haralick = np.zeros((4, 13)) + np.nan
        if tmp_haralick.shape != (4, 13):  tmp_haralick = np.zeros((4, 13)) + np.nan
        haralick[distIdx] = tmp_haralick
    haralick = np.nanmean(haralick,axis=0)

    return haralick


def call_haralick3(subimage):
    
    # FOR COMPUTING GLCM,
    # USE SCIKIT-IMAGE PACKAGE WHICH CAN HANDLE MULTIPLE CO-OCCURANCE DISTANCE.
    # FOR AVERAGNIG TEXTURE FEATURES FROM MULTIPLE DISTANCES, TAKE MEAN AT GLCM LEVEL
    
    cooccuranceDistances = range(1,np.min(subimage.shape)//2)
    directions = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcmDim = int(np.max(subimage)+1)
    glcm = greycomatrix( subimage, distances=cooccuranceDistances, \
                        angles=directions, levels=glcmDim, \
                        symmetric=True, normed=True )
    glcm = np.swapaxes(np.nanmean(glcm,axis=2).T,1,2)
    try:
        haralick = \
            mahotas.features.texture.haralick_features( glcm,ignore_zeros=True )
    except ValueError:
        haralick = np.zeros((4, 13)) + np.nan
    if haralick.shape != (4, 13):  haralick = np.zeros((4, 13)) + np.nan

    return haralick


def clf_predict(inputData):
    ''' Apply svm on some input data
    The is used for easy pickling (needed for multiprocessing)
    '''
    global clf
    return clf.predict(inputData)


def convert2gray(iarray, vmin, vmax, l):
    ''' Convert input data (float) to limited number of gray levels

    Parameters
    ----------
        iarray : ndarray
            2D input data (e.g. sigma0_HH_cor_db from Sentinel1Image)

        vmin : float
            minimum value used for scaling to gray levels
        vmax : float
            maximum values used for scaling to gray levels
        l : int
            number of gray levels
    Returns
    -------
        oarray : ndarray
            2D matrix with values of gray levels in UINT8 format
    '''
    
    # raise error if l is greater than 255.
    if l > 255:
        raise ValueError('maximum gray level cannot be greater than 255.')
    
    # convert to integer levels
    nanIdx = np.isnan(iarray)
    iarray = 1 + (l - 1) * (iarray - vmin) / (vmax - vmin)
    iarray[nanIdx] = 0
    iarray[iarray < 1] = 1
    iarray[iarray > l] = l
    iarray[nanIdx] = 0      # NaN -> 0.

    # return as unsigned integer
    return iarray.astype('uint8')


def get_texture_features(iarray, ws, stp, threads, alg):
    ''' Calculate Haralick texture features 
        using mahotas package and scikit-image package

    Parameters
    ----------
        iarray : ndarray
            2D input data with gray levels
        ws : int
            size of subwindow
        stp : int
            step of sub-window floating
        threads : int
            number of parallel processes
        alg : int
            algorithm selection for "call_haralick+[number]"
            0 : compute texture from single coocurrence distance (using MAHOTAS)
            1 : compute averaged texture from multi-coocurrence distance (using MAHOTAS)
            2 : compute averaged texture from multi-coocurrence distance by
                taking mean at Haralick feature level (using SCIKIT-IMAGE)
            3 : compute averaged texture from multi-coocurrence distance by
                taking mean at GLCM level (using SCIKIT-IMAGE)

    Returns
    -------
        harImageAnis : ndarray
            [13 x ROWS x COLS] array with texture features descriptors
            13 - nuber of texture features
            ROWS = rows of input image / stp
            COLS = rows of input image / stp
    '''
    # init parallel processing
    pool = Pool(threads)

    # apply calculation of Haralick texture features in many threads
    # in row-wise order
    call_haralick = eval('call_haralick%d' % alg)
    print('Compute GLCM and extract Haralick texture features')
    harList = []
    for r in range(0, iarray.shape[0]-ws-1, stp):
        sys.stdout.write('\rRow number: %5d' % r)
        sys.stdout.flush()
        # collect all subimages in the row into one list
        subImgs = [iarray[r:r+ws, c:c+ws] for c in range(0, iarray.shape[1]-ws-1, stp)]
        # calculate Haralick texture features in all sub-images in this row
        # using multiprocessing (parallel computing)
        harRow = pool.map(call_haralick, subImgs)
        # keep vectors with calculated texture features
        harList.append(np.array(harRow))
        # call_haralick should always return vector with size 4 x 13.
        # in unlikely case it fails raise an error
        if np.array(harRow).shape != (len(subImgs), 4, 13):
            raise
    print('...done.')

    # terminate parallel processing. THIS IS IMPORTANT!!!
    pool.close()

    # convert list with texture features to array
    harImage = np.array(harList)

    # calculate directional mean
    harImageAnis = harImage.mean(axis=2)

    pool.close()
    # reshape matrix and make images to be on the first dimension
    return np.swapaxes(harImageAnis.T, 1, 2)


def compute_transform_coeffs(tf, **kwargs):
    ''' Compute coefficients for texture feature transform and normalization
        
        Parameters
        ----------
        tf : ndarray
            1D vector of texture feature
        percentile : float, optional
            percentile to use for cliping extreme values. Default is 0.1.
        algorithm : str, optional
            transform type. Default is 'log'.
            'log'
                apply log transform for positively skewed data.
                apply exponential transform for negatively skewed data.
            'boxcox'
                apply Box-Cox transform and optimized lambda value
        skew_thres : float, optional
            skewness threshold for determining the application of transform.
            Data having skewness lower than this threshold will not be transformed.
            Default is 2.
        
        Returns
        -------
        newTF : ndarray
        3D matrix with normalized texture features (same size, dtype)
    '''

    for key in kwargs:
        if key not in [ 'percentile', 'algorithm' , 'skew_thres' ]:
            raise KeyError("compute_transform_coeffs() got an unexpected keyword argument '%s'" % key)

    if 'percentile' not in kwargs:
        kwargs['percentile'] = 0.1

    if 'algorithm' not in kwargs:
        kwargs['algorithm'] = 'log'
    elif kwargs['algorithm'] not in [ 'log' , 'boxcox' ]:
        raise KeyError("kwargs['algorithm'] got an invalid value '%s'"
                       % kwargs['algorithm'])

    if 'skew_thres' not in kwargs:
        kwargs['skew_thres'] = 2.

    percentile = np.abs(np.float(kwargs['percentile']))
    algorithm = kwargs['algorithm']
    skew_thres = np.abs(np.float(kwargs['skew_thres']))

    tfMin = np.nanmin(tf)
    tfMax = np.nanmax(tf)
    tfMean = np.nanmean(tf)
    tfSkew = skew(tf[np.isfinite(tf)])
    finiteIdx = np.isfinite(tf)

    if algorithm=='log':
        transPar2 = 0
        
        if tfSkew > skew_thres:
            print 'log-trans',
            transPar1 = - tfMin + 0.1 * np.abs(tfMean)
            newTF = np.log10(tf + transPar1)
        elif tfSkew < -skew_thres:
            print 'exp-trans',
            transPar1 = - tfMax
            newTF = 10 ** (tf + transPar1)
        else:
            print ' no trans',
            newTF = np.array(tf)
            transPar1 = 0

    elif algorithm=='boxcox':
    
        if abs(tfSkew) > skew_thres:
            print ' Box-Cox ',
            transPar1 = 1 - tfMin
            transTF, transPar2 = boxcox(tf[finiteIdx] + transPar1)
            newTF = np.ones_like(tf) * np.nan
            newTF[finiteIdx] = transTF
        else:
            print ' no trans',
            newTF = np.array(tf)
            transPar1 = 0
            transPar2 = 0

    newTFStd = np.nanstd(newTF)
    newTFMean = np.nanmean(newTF)
    newTF = (newTF - newTFMean) / newTFStd
    newTFMin, newTFMax = np.percentile(newTF[finiteIdx], (percentile, 100-percentile))
    newTFSkew = skew(newTF[finiteIdx])

    return newTF, [tfSkew, transPar1, transPar2, newTFMean, newTFStd], newTFSkew


def normalize_texture_features(tfs, normFile, **kwargs):
    ''' Transform, center on mean and normalize by STD each TF
        
        Load from prepared file values of transform coefficients, mean and STD for each TF
        
        Parameters
        ----------
            tfs : ndarray
                3D matrix with all texture features [13 x rows x cols]
            normFile : str
                name of file with log-flag, mean and STD
            algorithm : str, optional
                transform type. Default is 'log'.
                'log'
                    apply log transform for positively skewed data.
                    apply exponential transform for negatively skewed data.
                'boxcox'
                    apply Box-Cox transform using given lambda value in normFile
            skew_thres : float, optional
                skewness threshold for determining the application of transform.
                data having skewness lower than this threshold will not be transformed.
                Default is 2.
            
        Returns
        -------
            newTF : ndarray
                3D matrix with normalized texture features (same size, dtype)
        '''
    
    for key in kwargs:
        if key not in [ 'algorithm' , 'skew_thres' ]:
            raise KeyError("normalize_texture_features() got an unexpected keyword argument '%s'" % key)

    if 'algorithm' not in kwargs:
        kwargs['algorithm'] = 'log'
    elif kwargs['algorithm'] not in ['log','boxcox']:
        raise KeyError("kwargs['algorithm'] got an invalid value '%s'"
                       % kwargs['algorithm'])

    if 'skew_thres' not in kwargs:
        kwargs['skew_thres'] = 2.

    algorithm = kwargs['algorithm']
    skew_thres = np.abs(np.float(kwargs['skew_thres']))


    # load log-flag, mean and STD
    normCoefs = np.load(normFile)
    # make copy of tfs
    tfsNorm = np.array(tfs)

    print('---> TRANSFORM CODE = '),
    # log-transform or exp-transform if needed some of the TFs
    for i, tfSkew in enumerate(normCoefs[0]):
        if abs(tfSkew) < skew_thres:
            print('N'),
            continue
        elif algorithm=='log':
            if tfSkew > skew_thres:
                print('L'),
                tfsNorm[i] = np.log10(tfsNorm[i] + normCoefs[1,i]) + normCoefs[2,i]
            elif tfSkew < -skew_thres:
                print('E'),
                tfsNorm[i] = 10 ** (tfsNorm[i] + normCoefs[1,i]) + normCoefs[2,i]
        elif algorithm=='boxcox':
            print('B'),
            tfsNorm[i] = boxcox(tfsNorm[i] + normCoefs[1,i], lmbda=normCoefs[2,i])
    print('')

    # center at mean and normalize to STD
    tfsNorm = (tfsNorm - normCoefs[3][None][None].T) / normCoefs[4][None][None].T
    
    return tfsNorm


def apply_svm(tfs, svmFile, threads):
    ''' Apply SVM to normalized texture features and lable each vector

    Parameters
    ----------
        tfs : ndarray
            3D matrix with normalized texture features [features x rows x cols]
        svmFile : str
            name of file with pre-saved SVM
        threads : int
            number of threads for parallell computing
    Returns
    -------
        labels : ndarray
            1D vector with labels for each vector (or np.nan)
    '''
    global clf
    # load SVM from pre-saved file
    clf = pickle.load(open(svmFile, "rb" ))

    # reshape input 3D cube [features x rows x cols] int 2D matrix [feats x total_size]
    tfs2D = tfs.reshape(tfs.shape[0], tfs.shape[1] * tfs.shape[2])

    # find good data for processing (not NaN)
    gpi = np.isfinite(tfs2D.sum(axis=0))
    tfsGood = tfs2D[:, gpi]

    # split good data into chunks for parallel processing
    chunkSize = 1000
    tfsGoodChunks = [tfsGood[:, i:i+chunkSize].T
                         for i in range(0, tfsGood.shape[1], chunkSize)]

    # run parallel processing of all data with SVM
    pool = Pool(threads)
    svmLablesGood = pool.map(clf_predict, tfsGoodChunks)

    # join results back from the queue and insert into full matrix
    svmLabelsGood = np.hstack(svmLablesGood)
    svmLabelsAll = np.zeros(tfs2D.shape[1]) + np.nan
    svmLabelsAll[gpi] = svmLabelsGood

    # reshape labels from vector into 2D raster map
    return svmLabelsAll.reshape(tfs.shape[1], tfs.shape[2])


def get_map(s1i, bands, vmin, vmax,
                l=64, ws=32, stp=32, threads=2,
                normFiles=None, svmFile=None):
    '''Get raster map with classification results

    Parameters
    ----------
        s1i : Sentinel1Image
            Nansat chiled with SAR data
        bands : list of strings or integers
            IDs of bands to calculate texture features from
        vmin : list of floats
            minimum values used for scaling to gray levesl
        vmax : list of floats
            maximum values used for scaling to gray levesl
        l : int
            number of gray levels
        ws : int
            sub-window size to calculate textures in
        stp : int
            step of sub-window floating
        threads : int
            number of parallell processes
        normFiles : list of str
            name of file to use for normalization of texture features
        svmFile : str
            name of file where SVM is stored
    Returns
    -------
        map : ndarray
            raster map with classification results
            with size = input_image.shape() / stp
        '''

    # get water mask
    wm = s1i.watermask()[1]

    # container for texture features from all bands (e.g. both HH and HV)
    tfs = []
    for i, bandName in enumerate(bands):
        # get array from the band
        bandArray = s1i[bandName]

        # convert to gray levels
        bandArray = convert2gray(bandArray, vmin[i], vmax[i], l)

        # mask away land
        bandArray[wm == 2] = 0

        # get texture features
        tf = get_texture_features(bandArray, ws, stp, threads)

        # normalize texture features
        tf = normalize_texture_features(tf, normFiles[i])

        # append texture features as 2D matrix [13 x total_size]
        tfs.append(tf)

    # stack texture features from all bands into single 3D matrix
    # if two input bands only (e.g. HH and HV), size is [26 x rows x cols]
    tfs = np.vstack(tfs)

    # apply SVM
    lables = apply_svm(tfs, svmFile, threads)

    return lables


def createKernel(radius):
    
    kernel = np.zeros((2*radius+1, 2*radius+1))
    y,x = np.ogrid[-radius:radius+1, -radius:radius+1]
    mask = x**2 + y**2 <= radius**2
    kernel[mask] = 1
    
    return kernel


def bufferMask(inputMask,bufferSize):
    
    return morphology.binary_dilation(inputMask,structure=createKernel(bufferSize))


def convert2fullres(inArray,outDim,comp_fac):
    
    inArray = np.array(inArray)
    inDim = inArray.shape
    outArray = np.ones(outDim) * np.nan
    outArray_chunks = [ x * np.ones((comp_fac,comp_fac))
                        for x in inArray.flatten() ]
    outArray = ( np.concatenate( np.array_split( np.concatenate( outArray_chunks,
                     axis=1 ), inDim[0], axis=1 ), axis=0 )
                 [:inDim[0]*comp_fac,:inDim[1]*comp_fac] )

    return outArray


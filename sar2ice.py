import os, sys, glob, mahotas, pickle, time
import numpy as np
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from multiprocessing import Pool
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from skimage.feature import greycomatrix
from scipy.ndimage import morphology, maximum_filter
from scipy.stats import skew, boxcox
from operator import add
from nansat import Nansat, Domain
from PIL import Image
clf = None



# GLCM computation result from MAHOTAS is different from that of SCIKIT-IMAGE.
# MAHOTAS considers distance as number of cells in given direction.
# SCKIT-IMAGE considers distance as euclidian distance, and take values form
# the nearest neighbor when the euclidian distance is not integer.
# e.g.) reference cell coordinate (100,100), direction = 45 deg., distance = 3
# MAHOTAS counts co-occurence pair between (100,100) and (103,103).
# SCIKIT-IMAGE counts co-occurence pair between (100,100) and (102,102), because
# a euclidian distance of 3 in direction of 45 degree corresponds to 3/sqrt(2),
# which is 2.121 along x and y coordinate, and 2.12 is closer to 2 rather than 3.


def haralick_averagedGLCM(subimage):

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


def haralick_AveragedTFs(subimage):

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
        alg : str
            'averagedGLCM' : compute averaged texture from multi-coocurrence 
                             distance by taking mean at Haralick feature level
            'averagedTFs' : compute averaged texture from multi-coocurrence 
                            distance by taking mean at GLCM level

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
    call_haralick = eval('haralick_'+alg)
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
        algorithm : str, optional
            transform type. Default is 'log'.
            'log'
                apply log transform for positively skewed data.
                apply exponential transform for negatively skewed data.
            'boxcox'
                apply Box-Cox transform and optimized lambda value
        
        Returns
        -------
        newTF : ndarray
            1D vector of normalized texture feature (same size, dtype)
        normCoeffs : ndarray
            1D vector of five normalization coefficients
    '''

    for key in kwargs:
        if key not in [ 'algorithm' , 'ignore_value' ]:
            raise KeyError("compute_transform_coeffs() got an unexpected keyword argument '%s'" % key)

    if 'algorithm' not in kwargs:
        kwargs['algorithm'] = 'boxcox'
    elif kwargs['algorithm'] not in [ 'log' , 'boxcox' ]:
        raise KeyError("kwargs['algorithm'] got an invalid value '%s'"
                       % kwargs['algorithm'])
    algorithm = kwargs['algorithm']

    tf = tf[np.isfinite(tf)]
    tfMin,tfMax = np.min(tf), np.max(tf)
    tfSkew = skew(tf)
    tfMean = np.mean(tf)

    if algorithm=='log':
        transPar2 = 0
        
        if tfSkew > 0:
            print 'log-trans',
            transPar1 = - tfMin + 0.1 * np.abs(tfMean)
            newTF = np.log10(tf + transPar1)
        elif tfSkew < 0:
            print 'exp-trans',
            transPar1 = - tfMax
            newTF = 10 ** (tf + transPar1)
        else:
            print ' no trans',
            newTF = np.array(tf)
            transPar1 = 0

    elif algorithm=='boxcox':
    
        print ' Box-Cox ',
        transPar1 = 1 - tfMin
        newTF, transPar2 = boxcox(tf + transPar1)

    newTFStd = np.std(newTF)
    newTFMean = np.mean(newTF)
    newTF = (newTF - newTFMean) / newTFStd

    return newTF, [tfSkew, transPar1, transPar2, newTFMean, newTFStd]


def normalize_texture_features(tfs, normFile, skew_thres=0):
    ''' Transform, center on mean and normalize by STD each TF
        
        Load from prepared file values of transform coefficients, mean and STD for each TF
        
        Parameters
        ----------
            tfs : ndarray
                3D matrix with all texture features [13 x rows x cols]
            normFile : str
                name of file with log-flag, mean and STD
            skew_thres : float, optional
                skewness threshold for determining the application of transform.
                data having skewness lower than this threshold will not be transformed.
                Default is 0
            
        Returns
        -------
            newTF : ndarray
                3D matrix with normalized texture features (same size, dtype)
        '''
    

    skew_thres = np.abs(np.float(skew_thres))

    # load log-flag, mean and STD
    algorithm = np.load(normFile)['normAlg']
    normCoeffs = np.load(normFile)['normCoeffs']
    
    # make copy of tfs
    tfsNorm = np.array(tfs)

    print('---> TRANSFORM CODE = '),
    # log-transform or exp-transform if needed some of the TFs
    for i, tfSkew in enumerate(normCoeffs[:,0]):
        if abs(tfSkew) < skew_thres:
            print('N'),
            continue
        elif algorithm=='log':
            if tfSkew > skew_thres:
                print('L'),
                tfsNorm[i] = np.log10(tfsNorm[i] + normCoeffs[i,1]) + normCoeffs[i,2]
            elif tfSkew < -skew_thres:
                print('E'),
                tfsNorm[i] = 10 ** (tfsNorm[i] + normCoeffs[i,1]) + normCoeffs[i,2]
        elif algorithm=='boxcox':
            print('B'),
            tfsNorm[i] = boxcox(tfsNorm[i] + normCoeffs[i,1], lmbda=normCoeffs[i,2])
    print('')

    # center at mean and normalize to STD
    tfsNorm = (tfsNorm - normCoeffs[:,3][None][None].T) / normCoeffs[:,4][None][None].T
    
    return tfsNorm


def apply_pca_Kmeans(tfs,tfID,nPC,pcID,nCluster):
    ''' Apply PCA and Kmeans clustering to normalized texture features

    Parameters
    ----------
        tfs : ndarray
            3D matrix with normalized texture features [features x rows x cols]
        tfID : list of int
            texture feature ID to use for PCA
        nPC : int
            number of PC
        pcID : list of int
            PC ID to use for Kmeans clustering
        nCluster : int
            number of cluster
    Returns
    -------
        labels : ndarray
            nPC * 2D raster map with labels (or np.nan)
    '''
    tfs2D = tfs.reshape(tfs.shape[0], tfs.shape[1] * tfs.shape[2])
    gpi = np.isfinite(tfs2D.sum(axis=0))
    pcaDataGood = PCA(n_components=nPC).fit_transform(tfs2D[:,gpi].T)
    labelsGood = KMeans(n_clusters=nCluster).fit_predict(pcaDataGood[:,pcID])
    pcaDataAll = np.zeros((nPC, tfs2D.shape[1])) + np.nan
    pcaDataAll[:,gpi] = pcaDataGood.T
    labelsAll = np.zeros(tfs2D.shape[1]) + np.nan
    labelsAll[gpi] = labelsGood

    return labelsAll.reshape(tfs.shape[1],tfs.shape[2])


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
            2D raster map with labels (or np.nan)
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


def get_map(s1i,env):
    '''Get raster map with classification results

    Parameters
    ----------
        s1i : Sentinel1Image
            Nansat chiled with SAR data
        env['mLook'] : int
            multi-look factor
        env['vmin'] : list of floats
            minimum values used for scaling to gray levesl
        env['vmax'] : list of floats
            maximum values used for scaling to gray levesl
        env['l'] : int
            number of gray levels
        env['ws'] : int
            sub-window size to calculate textures in
        env['stp'] : int
            step of sub-window floating
        env['tfAlg'] : str
            texture feature extraction algorithm. 
            choose from ['averagedGLCM','averagedTFs']
        env['textureFeatureID'] : list of int
            texture feature ID to use for PCA
        env['numberOfPrincialComponent'] : int
            number of PC
        env['princialComponentID'] : list of int
            PC ID to use for Kmeans clustering
        env['numberOfKmeansCluster'] : int
            number of cluster
        env['threads'] : int
            number of parallell processes
        env['normFiles'] : list of str
            name of file to use for normalization of texture features
        env['svmFile'] : str
            name of file where SVM is stored
    Returns
    -------
        sigma0 : ndarray
            raster map with gray-level converted backscattering coefficients
        tfs : ndarray
            raster map with texture features
        pca_labels : ndarray
            raster map with PCA based clustering results
            with size = input_image.shape() / stp
        svm_labels : ndarray
            raster map with SVM based classification results
            with size = input_image.shape() / stp
        '''

    mLook = env['multiLookFactor']
    vmax = env['sigma0_max']
    vmin = env['sigma0_min']
    l   = env['grayLevel']    # gray-level. 32 or 64.
    ws  = env['subwindowSize']    # 1km pixel spacing (40m * 25 = 1000m)
    stp = env['stepSize']    # step size
    tfAlg = env['textureFeatureAlgorithm']
    tfID = env['textureFeatureID']
    nPC = env['numberOfPrincialComponent']
    pcID = env['princialComponentID']
    nCluster = env['numberOfKmeansCluster']
    threads = env['numberOfThreads']
    normFiles = { 'HH':env['textureFeatureNormalizationFilePrefix']+'HH.npz',
                  'HV':env['textureFeatureNormalizationFilePrefix']+'HV.npz' }
    svmFile = env['supportVectorMachineFile']

    print('denoising and multi-look ...')
    for pol in ['HH','HV']:
        s1i.add_denoised_band( 'sigma0_%s' % pol,
            denoAlg='NERSC', addPow='EW0', clipDirtyPx=True, adaptNoiSc=False,
            angDepCor=True, fillVoid=False, dBconv=False, development=True )
    skipGCPs = 4          # choose from [1,2,4,5]
    if mLook!=1:
        skipGCPs = np.ceil(skipGCPs/float(mLook))
        s1i.resize(factor=1./mLook)

    print('watermask generation ... ')
    nGCPs = s1i.vrt.dataset.GetGCPCount()
    GCPs = s1i.vrt.dataset.GetGCPs()
    idx = np.arange(0,nGCPs).reshape(nGCPs//21,21)
    skipGCPsRow = max( [ y for y in range(1,nGCPs//21)
                         if ((nGCPs//21 -1) % y == 0) and y <= skipGCPs ] )
    smpGCPs = [ GCPs[i] for i in np.concatenate(idx[::skipGCPsRow,::skipGCPs]) ]
    GCPProj = s1i.vrt.dataset.GetGCPProjection()
    dummy = s1i.vrt.dataset.SetGCPs(smpGCPs,GCPProj)
    watermask = s1i.watermask(tps=True)[1]
    dummy = s1i.vrt.dataset.SetGCPs(GCPs,GCPProj)

    print('texture feature extraction and normalization ...')
    sigma0 = {'HH':[],'HV':[]}
    tfs = []
    for pol in ['HH','HV']:
        sigma0[pol] = 10*np.log10(s1i['sigma0_%s_denoised' % pol])
        sigma0[pol] = convert2gray(sigma0[pol],vmin[pol],vmax[pol],l)
        sigma0[pol][maximum_filter(watermask==2,ws)] = 0
        tf = get_texture_features(sigma0[pol],ws,stp,threads,tfAlg)
        tf = normalize_texture_features(tf,normFiles[pol],skew_thres=0)
        tfs.append(tf)
    tfs = np.vstack(tfs)
    inc_ang0 = np.nanmean(s1i['incidence_angle'],axis=0)
    inc_ang = np.array([
        np.mean(inc_ang0[c:c+ws]) for c in range(0,inc_ang0.shape[0]-ws-1,stp) ])
    inc_ang = np.ones((tfs.shape[1],1))*inc_ang[np.newaxis,:]

    ssw0 = s1i['subswath_indices'].astype(float)
    ssw0[ssw0==0] = np.nan
    ssw = np.ones(tfs.shape[1:])*np.nan
    for i,r in enumerate(range(0, ssw0.shape[0]-ws-1, stp)):
        ssw[i,:] = [ np.nanmean(ssw0[r:r+ws,c:c+ws])
                     for c in range(0, ssw0.shape[1]-ws-1, stp) ]

    print('apply PCA and Kmeans clustering ...')
    pca_labels = apply_pca_Kmeans(tfs, tfID, nPC, pcID, nCluster)
    print('apply SVM ...')
    svm_labels = apply_svm(np.vstack([tfs,inc_ang[None],ssw[None]]), svmFile, threads)

    return sigma0,tfs,pca_labels,svm_labels


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
    outArray = ( np.concatenate( np.array_split( np.concatenate(
                     outArray_chunks, axis=1 ),inDim[0], axis=1 ), axis=0 )
                 [:outDim[0],:outDim[1]] )

    return outArray


def fixedPatchProc(inputDataArray,inputSWindexArray,function,windowSize):
    
    function = eval(function)
    nRowsOrig, nColsOrig = inputDataArray.shape
    nRowsProc = (nRowsOrig//windowSize+bool(nRowsOrig%windowSize))*windowSize
    nColsProc = (nColsOrig//windowSize+bool(nColsOrig%windowSize))*windowSize
    dataChunks = np.ones((nRowsProc,nColsProc))*np.nan
    dataChunks[:nRowsOrig,:nColsOrig] = inputDataArray.copy()
    SWindexChunks = np.ones((nRowsProc,nColsProc))*np.nan
    SWindexChunks[:nRowsOrig,:nColsOrig] = inputSWindexArray.copy()
    del inputDataArray, inputSWindexArray

    dataChunks = [ dataChunks[i*windowSize:(i+1)*windowSize,
                              j*windowSize:(j+1)*windowSize]
                   for (i,j) in np.ndindex(nRowsProc//windowSize,
                                           nColsProc//windowSize) ]
    SWindexChunks = [ SWindexChunks[i*windowSize:(i+1)*windowSize,
                                    j*windowSize:(j+1)*windowSize]
                      for (i,j) in np.ndindex(nRowsProc//windowSize,
                                              nColsProc//windowSize) ]

    def subfunc_fixedPatchProc(inputDataChunk,inputSWindexChunk):
        outputDataChunk = np.ones_like(inputDataChunk)*np.nan
        uniqueIndices = np.unique(inputSWindexChunk)
        uniqueIndices = uniqueIndices[uniqueIndices>0]  # ignore 0
        for uniqueIndex in uniqueIndices:
            mask = (inputSWindexChunk==uniqueIndex)*np.isfinite(inputDataChunk)
            outputDataChunk[mask] = function(inputDataChunk[mask])
        return np.nanmean(outputDataChunk)

    outputDataArray = map( subfunc_fixedPatchProc, dataChunks, SWindexChunks )
    del dataChunks,SWindexChunks
    outputDataArray = (
        np.reshape(outputDataArray,[nRowsProc//windowSize,nColsProc//windowSize])
        )[:nRowsOrig//windowSize,:nColsOrig//windowSize]

    return outputDataArray


def slidingPatchProc(inputDataArray,inputSWindexArray,function,windowSize):
    
    if windowSize%2 != 1:
        raise ValueError('windowSize must be odd number.')
    hWin = int(windowSize)/2
    function = eval(function)
    nRowsOrig, nColsOrig = inputDataArray.shape
    nRowsProc = nRowsOrig+2*hWin
    nColsProc = nColsOrig+2*hWin
    dataArray = np.ones((nRowsProc,nColsProc))*np.nan
    dataArray[hWin:-hWin,hWin:-hWin] = inputDataArray.copy()
    SWindexArray = np.ones((nRowsProc,nColsProc))*np.nan
    SWindexArray[hWin:-hWin,hWin:-hWin] = inputSWindexArray.copy()
    outputDataArray = np.ones((nRowsProc,nColsProc))*np.nan
    del inputDataArray, inputSWindexArray
    
    def subfunc_movingPatchProc(inputDataChunk,inputSWindexChunk):
        outputData = np.ones_like(inputDataChunk)*np.nan
        uniqueIndices = np.unique(inputSWindexChunk)
        uniqueIndices = uniqueIndices[uniqueIndices>0]  # ignore 0
        for uniqueIndex in uniqueIndices:
            mask = (inputSWindexChunk==uniqueIndex)*np.isfinite(inputDataChunk)
            outputData[mask] = function(inputDataChunk[mask])
        return np.nanmean(outputData)

    for ir in range(hWin,nRowsProc-hWin):
        dataChunks = [ dataArray[ir-hWin:ir+hWin+1,ic-hWin:ic+hWin+1]
                       for ic in range(hWin,nColsProc-hWin) ]
        SWindexChunks = [ SWindexArray[ir-hWin:ir+hWin+1,ic-hWin:ic+hWin+1]
                          for ic in range(hWin,nColsProc-hWin) ]
        outputDataArray[ir,hWin:-hWin] = map(
            subfunc_movingPatchProc, dataChunks,SWindexChunks )

    return outputDataArray[hWin:-hWin,hWin:-hWin]


def export_PS_proj_GTiff(inputArray,sourceFilename,outputFilename):
    
    ### NaN is replaced by zero.
    originalCmap = plt.rcParams['image.cmap']
    plt.rcParams['image.cmap'] = 'jet'
    inputArray = np.array( (inputArray-np.nanmin(inputArray))
        / (np.nanmax(inputArray)-np.nanmin(inputArray)) * 254 +1, dtype='uint8')
    srcNansatObj = Nansat(sourceFilename)
    resizeFac = srcNansatObj.shape()[1] / inputArray.shape[1]
    srcNansatObj.crop(0,0,srcNansatObj.shape()[1]/resizeFac*resizeFac,
                          srcNansatObj.shape()[0]/resizeFac*resizeFac)
    srcNansatObj.resize(1./resizeFac)
    newNansatObj = Nansat( domain=srcNansatObj, array= inputArray,
                           parameters={'name':'new_band'} )
    newDomain = Domain("+proj=stere +lat_0=90 +lat_ts=71 +lon_0=0 +k=1 "
                       + "+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs",
                       ds=srcNansatObj.vrt.dataset)
    newNansatObj.reproject(newDomain)
    newNansatObj.write_geotiffimage(outputFilename,'new_band')
    plt.rcParams['image.cmap'] = originalCmap


def export_uint8_png(outputFilename,inputData,cmap='jet',**kwargs):
    
    ### NaN is replaced by zero.
    if 'vmin' not in kwargs:
        kwargs['vmin'] = float(np.nanmin(inputData))
    if 'vmax' not in kwargs:
        kwargs['vmax'] = float(np.nanmax(inputData))
    cfunc = eval('matplotlib.cm.'+cmap)
    uint8Data = ( cfunc( (inputData-kwargs['vmin'])
                      /(kwargs['vmax']-kwargs['vmin']))*254+1 ).astype(np.uint8)
    uint8Data[np.isnan(inputData)] = [0,0,0,0]
    RGBA = Image.fromarray(uint8Data)
    RGBA.save(outputFilename,transparant=(0,0,0,0))


def export_uint8_jpeg(outputFilename,inputData,**kwargs):
    
    ### NaN is replaced by zero.
    if 'vmin' not in kwargs:
        kwargs['vmin'] = float(np.nanmin(inputData))
    if 'vmax' not in kwargs:
        kwargs['vmax'] = float(np.nanmax(inputData))
    uint8Data = (inputData-kwargs['vmin'])/(kwargs['vmax']-kwargs['vmin'])*254+1
    uint8Data[uint8Data>255] = 255
    uint8Data[uint8Data<1] = 1
    uint8Data = uint8Data.astype(np.uint8)
    GRAY = Image.fromarray(uint8Data).save(outputFilename)

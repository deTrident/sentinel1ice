from __future__ import print_function
import os, sys, glob, mahotas, pickle
import numpy as np
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from multiprocessing import Pool
from skimage.feature import greycomatrix
from scipy.ndimage import maximum_filter
from operator import add
from nansat import Nansat, Domain
from datetime import datetime
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


def convert2gray(iarray, vmin, vmax, l):
    ''' Convert input data (float) to limited number of gray levels

    Parameters
    ----------
        iarray : ndarray
            2D input data

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
    for r in range(0, iarray.shape[0]-ws+1, stp):
        sys.stdout.write('\rRow number: %5d' % r)
        sys.stdout.flush()
        # collect all subimages in the row into one list
        subImgs = [iarray[r:r+ws, c:c+ws] for c in range(0, iarray.shape[1]-ws+1, stp)]
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


def get_map(s1i,env):
    '''Get raster map with classification results

    Parameters
    ----------
        s1i : Sentinel1Image
            Nansat class with SAR data
        env['gamma0_min'] : list of floats
            minimum values used for scaling to gray levels
        env['gamma0_max'] : list of floats
            maximum values used for scaling to gray levels
        env['grayLevel'] : int
            number of gray levels
        env['subwindowSize'] : int
            sub-window size to calculate textures in
        env['stepSize'] : int
            step of sub-window floating
        env['textureFeatureAlgorithm'] : str
            texture feature extraction algorithm. 
            choose from ['averagedGLCM','averagedTFs']
        env['numberOfThreads'] : int
            number of parallell processes
        env['classifierFilename'] : str
            name of file where SVM is stored
    Returns
    -------
        s1i : Sentinel1Image
            Nansat class with processed data
    '''
    gamma0_max = env['gamma0_max']
    gamma0_min = env['gamma0_min']
    l   = env['grayLevel']    # gray-level. 32 or 64.
    ws  = env['subwindowSize']    # 1km pixel spacing (40m * 25 = 1000m)
    stp = env['stepSize']    # step size
    tfAlg = env['textureFeatureAlgorithm']
    threads = env['numberOfThreads']
    classifierFilename = env['classifierFilename']

    print('*** denoising ...')
    gamma0 = {'HH':[],'HV':[]}
    for pol in ['HH','HV']:
        s1i.add_band(array=(s1i.thermalNoiseRemoval_dev(polarization=pol, windowSize=ws)
                            / np.cos(np.deg2rad(s1i['incidence_angle']))),
                     parameters={'name': 'gamma0_%s_denoised' % pol})
    skipGCPs = 4          # choose from [1,2,4,5]
    nGCPs = s1i.vrt.dataset.GetGCPCount()
    GCPs = s1i.vrt.dataset.GetGCPs()
    idx = np.arange(0,nGCPs).reshape(nGCPs//21,21)
    skipGCPsRow = max( [ y for y in range(1,nGCPs//21)
                     if ((nGCPs//21 -1) % y == 0) and y <= skipGCPs ] )
    smpGCPs = [ GCPs[i] for i in np.concatenate(idx[::skipGCPsRow,::skipGCPs]) ]
    GCPProj = s1i.vrt.dataset.GetGCPProjection()
    dummy = s1i.vrt.dataset.SetGCPs(smpGCPs,GCPProj)
    s1i.add_band(array=s1i.watermask(tps=True)[1], parameters={'name': 'watermask'})
    dummy = s1i.vrt.dataset.SetGCPs(GCPs,GCPProj)

    print('*** texture feature extraction ...')
    tfs = {'HH':[],'HV':[]}
    for pol in ['HH','HV']:
        grayScaleImage = convert2gray(10*np.log10(s1i['gamma0_%s_denoised' % pol]),
                                      gamma0_min[pol], gamma0_max[pol], l)
        grayScaleImage[maximum_filter(s1i['watermask']==2,ws)] = 0
        tfs[pol] = get_texture_features(grayScaleImage, ws, stp, threads, tfAlg)
    s1i.resize(factor=1./stp)
    for pol in ['HH','HV']:
        for li in range(13):
            s1i.add_band(array=np.squeeze(tfs[pol][li,:,:]),
                         parameters={'name': 'Haralick_%02d_%s' % (li+1, pol)})

    print('*** applying SVM ...')
    plk = pickle.load(open(classifierFilename, "rb" ))
    if type(plk)==list:
        scaler, clf = plk
    else:
        class dummy_class(object):
            def transform(self, x):
                return(x)
        scaler = dummy_class()
        clf = plk
    clf.n_jobs = threads
    features = np.vstack([tfs['HH'], tfs['HV'], s1i['incidence_angle'][np.newaxis,:,:]])
    features = features.reshape((27,np.prod(s1i.shape()))).T
    gpi = np.isfinite(features.sum(axis=1))
    classImage = np.ones(np.prod(s1i.shape())) * np.nan
    classImage[gpi] = clf.predict(scaler.transform(features[gpi,:]))
    classImage = classImage.reshape(s1i.shape())
    s1i.add_band(array=classImage, parameters={'name': 'class'})

    return s1i


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

    outputDataArray = list(map( subfunc_fixedPatchProc, dataChunks, SWindexChunks ))
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
        outputDataArray[ir,hWin:-hWin] = list(map(
            subfunc_movingPatchProc, dataChunks,SWindexChunks ))

    return outputDataArray[hWin:-hWin,hWin:-hWin]


def julian_date(YYYYMMDDTHHMMSS):
    if not isinstance(YYYYMMDDTHHMMSS, str):
        raise ValueError('input instance YYYYMMDDTHHMMSS must be string.')
    year = int(YYYYMMDDTHHMMSS[:4])
    month = int(YYYYMMDDTHHMMSS[4:6])
    if month <= 2:
        year = year - 1
        month = month + 12
    dayFraction = ( int(YYYYMMDDTHHMMSS[9:11]) + int(YYYYMMDDTHHMMSS[11:13]) / 60.
                    + int(YYYYMMDDTHHMMSS[13:15]) / 3600. ) / 24.
    day = (   np.floor(365.25 * (year + 4716.0))
            + np.floor(30.6001 * (month + 1.0))
            + 2.0
            - np.floor(year / 100.0)
            + np.floor( np.floor(year / 100.0) / 4.0 )
            + int(YYYYMMDDTHHMMSS[6:8])
            - 1524.5 )
    return dayFraction + day


colorDict = { 'AARI':{ 0:(255, 255, 255),    # unclassified
                      -9:( 39, 189, 255),    # open water
                      82:(  0,  79, 255),    # nilas
                      83:(244,   0, 255),    # young ice
                      86:( 43, 191, 141),    # first year ice
                      95:(122,   0,   0),    # old ice
                      99:(150, 150, 150),    # fast ice
                      92:( 32, 135,   0),    # ice concentration 10-60 % (used only in this script)
                      94:(248, 101,   0), }, # ice concentration 70-100 % (used only in this script)
               'CIS':{ 0:(255, 255, 255),    # unclassified
                      81:(107,  34, 207),    # Gray ice
                      84:(107,  34, 207),    # Gray ice
                      85:(206,  52, 238),    # Gray-white ice
                      87:(145, 207,   0),    # Thin first year ice
                      91:( 47, 198,   0),    # Medium first year ice
                      93:( 25, 106,   0),    # Thick first year ice
                      95:(161,  77,  35),    # Old ice
                      99:(134, 194, 255), }  # open water
}



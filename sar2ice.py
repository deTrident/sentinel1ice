from __future__ import print_function
import os, sys, glob, pickle
from datetime import datetime
from multiprocessing import Pool
from operator import add

import numpy as np
import mahotas
import matplotlib.pyplot as plt
from skimage.feature import greycomatrix
from scipy.ndimage import maximum_filter
import gdal

from nansat import Nansat, Domain
from sentinel1corrected.S1_TOPS_GRD_NoiseCorrection import Sentinel1Image

clf = None

colorDict = {   0:(  0, 100, 255),    # Ice free
                1:(150, 200, 255),    # <1/10 ice of unspecified SoD (open water)
               81:(240, 210, 250),    # New ice
               82:(255, 138, 255),    # Nilas, Ice Rind
               83:(170,  40, 240),    # Young ice
               84:(135,  60, 215),    # Grey ice
               85:(220,  80, 235),    # Grey-white ice
               86:(255, 255,   0),    # First-year ice (FY)
               87:(155, 210,   0),    # FY thin ice (white ice)
               88:(215, 250, 130),    # FY thin ice (white ice) first stage
               89:(175, 250,   0),    # FY thin ice (white ice) second stage
               91:(  0, 200,  20),    # FY medium ice
               93:(  0, 120,   0),    # FY thick ice
               95:(180, 100,  50),    # Old ice
               96:(255, 120,  10),    # Second-year ice
               97:(200,   0,   0),    # Multi-year ice
               98:(210, 210, 210),    # Glacier ice
               99:(255, 255, 255),    # Ice of undefined SoD
              107:(150, 150, 150),    # Fast ice of unspecified SoD
              108:(255,   0,   0),    # Iceberg
              255:(  0,   0,   0),    # void cell in texture features (land, scene border)
}


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


def haralick_averagedTFs(subimage):

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


def save_texture_features_old(inp_file, subwindowSize, stepSize, numberOfThreads,
                          textureFeatureAlgorithm, quicklook, force):
    """ Wrapper around get_texture_features. Load input file, calculate TF, save output
    Parameters
    ----------
        inp_file : str
            name of inputfile
        subwindowSize : int
            size of subwindow
        stepSize : int
            step of sub-window floating
        numberOfThreads : int
            number of parallel processes
        textureFeatureAlgorithm : str
            'averagedGLCM' : compute averaged texture from multi-coocurrence
                             distance by taking mean at Haralick feature level
            'averagedTFs' : compute averaged texture from multi-coocurrence
                            distance by taking mean at GLCM level
        quicklook : bool
            generate quicklooks?
        force : bool
            force reprocessing?

    Returns
    -------
        harImageAnis : ndarray
            [13 x ROWS x COLS] array with texture features descriptors
            13 - nuber of texture features
            ROWS = rows of input image / stp
            COLS = rows of input image / stp
    """

    out_file = inp_file.replace('_sigma0','_texture_features')
    if os.path.exists(out_file) and not force:
        print('File %s with texture features already exists.' % out_file)
        return out_file

    print('Processing texture from ', inp_file)
    npz = np.load(inp_file)
    tfs = {}
    for pol in ['HH', 'HV']:
        print('Compute texture %s features from %s' % (pol, inp_file))
        # get texture features
        tfs[pol] = get_texture_features(npz['sigma0_%s' % pol], subwindowSize, stepSize,
                                        numberOfThreads, textureFeatureAlgorithm)
        
    if quicklook:
        # save each texture feature in a PNG
        for li in range(13):
            valid = np.isfinite(tfs['HH'][li] * tfs['HV'][li])
            for pol in ['HH', 'HV']:
                tf = tfs[pol][li]
                vmin, vmax = np.percentile(tf[valid], (1, 99))
                plt.imsave(out_file.replace('_texture_features.npz','_%s_har%02d.png' % (pol, li)),
                           tf, vmin=vmin, vmax=vmax )

    # save the results as a npz file
    np.savez_compressed(out_file, textureFeatures=tfs)

    return out_file


def save_texture_features(inp_file, subwindowSize, stepSize, numberOfThreads,
                          textureFeatureAlgorithm, quicklook, force):
    """ Wrapper around get_texture_features. Load input file, calculate TF, save output
    Parameters
    ----------
        inp_file : str
            name of inputfile
        subwindowSize : int
            size of subwindow
        stepSize : int
            step of sub-window floating
        numberOfThreads : int
            number of parallel processes
        textureFeatureAlgorithm : str
            'averagedGLCM' : compute averaged texture from multi-coocurrence
                             distance by taking mean at Haralick feature level
            'averagedTFs' : compute averaged texture from multi-coocurrence
                            distance by taking mean at GLCM level
        quicklook : bool
            generate quicklooks?
        force : bool
            force reprocessing?

    Returns
    -------
        harImageAnis : ndarray
            [13 x ROWS x COLS] array with texture features descriptors
            13 - nuber of texture features
            ROWS = rows of input image / stp
            COLS = rows of input image / stp
    """

    out_file = inp_file.replace('_sigma0','_texture_features')
    if os.path.exists(out_file) and not force:
        print('File %s with texture features already exists.' % out_file)
        return out_file

    print('Processing texture from ', inp_file)
    npz = np.load(inp_file)
    tfs = {}
    tmp_tfs = {}
    for pol in ['HH', 'HV']:
        for dtype in ['raw', 'denoised']:
            key = '%s_%s' % (pol, dtype)
            # get texture features
            data = npz['sigma0_%s' % key]
            swi = npz['subswathIndices']
            nSW = np.unique(swi)
            nRows = data.shape[0]//stepSize
            nCols = data.shape[1]//stepSize
            tmp_tfs[key] = np.ones((5, 13, nRows, nCols)) * np.nan
            for iSW in nSW[nSW>0]:
                print('Compute %s texture features of the subswath %s' % (key, iSW))
                w = np.reshape(
                        [(swi[r*stepSize:(r+1)*stepSize,c*stepSize:(c+1)*stepSize]==iSW).sum()
                         for (r,c) in np.ndindex(nRows, nCols)], (nRows, nCols)) / stepSize**2
                w = np.tile(w, (13,1,1))
                ri = np.where(swi==iSW)[1]
                riMin, riMax = ri.min()//stepSize*stepSize, (ri.max()//stepSize+1)*stepSize
                sswd = np.copy(data[:,riMin:riMax]).astype(np.int16)
                sswi = np.copy(swi[:,riMin:riMax])
                sswd[(sswi!=iSW) * (sswi!=0)] = -1
                nr = sswd.shape[1]
                for li in range(sswd.shape[0]):
                    fi = np.where(sswd[li]!=-1)[0]
                    if len(fi)==0:
                        continue
                    fiMin, fiMax = fi.min(), fi.max()
                    if fiMax!=(nr-1):
                        sswd[li][fiMax+1:nr] = sswd[li][fiMax:fiMax-(nr-fiMax)+1:-1]
                    if fiMin!=0:
                        sswd[li][0:fiMin] = sswd[li][fiMin:fiMin+fiMin]
                tmp_tfs[key][iSW-1,:,:,riMin//stepSize:riMax//stepSize] = ( get_texture_features(
                        sswd, subwindowSize, stepSize, numberOfThreads, textureFeatureAlgorithm)
                    * w[:,:,riMin//stepSize:riMax//stepSize] )
            invalid = np.isnan(np.nanmean(tmp_tfs[key],axis=0))
            tmp_tfs[key] = np.nansum(tmp_tfs[key],axis=0)
            tmp_tfs[key][invalid] = np.nan
        tfs[pol] = np.copy(tmp_tfs[pol+'_denoised'])
        # the thrid tfs (correlation) should be taken from the raw image
        tfs[pol][2] = np.copy(tmp_tfs[pol+'_raw'][2])

    # estimate scaling factor from HH, then apply it to the last two tfs of raw HV
    r = tmp_tfs['HH_denoised'][-1]/tmp_tfs['HH_raw'][-1]
    p = np.nanmedian(r[r!=1])   # r!=1 in the first subswath
    w1 = np.reshape([(swi[r*stepSize:(r+1)*stepSize,c*stepSize:(c+1)*stepSize]==1).sum()
             for (r,c) in np.ndindex(nRows, nCols)], (nRows, nCols)) / stepSize**2
    w2 = np.reshape([(swi[r*stepSize:(r+1)*stepSize,c*stepSize:(c+1)*stepSize]>=2).sum()
             for (r,c) in np.ndindex(nRows, nCols)], (nRows, nCols)) / stepSize**2
    tfs['HV'][-1] = tmp_tfs['HV_raw'][-1]*w1*p + tmp_tfs['HV_raw'][-1]*w2
    r = tmp_tfs['HH_denoised'][-2]/tmp_tfs['HH_raw'][-2]
    p = np.nanmedian(r[r!=1])   # r!=1 in the first subswath
    w1 = np.reshape([(swi[r*stepSize:(r+1)*stepSize,c*stepSize:(c+1)*stepSize]==1).sum()
             for (r,c) in np.ndindex(nRows, nCols)], (nRows, nCols)) / stepSize**2
    w2 = np.reshape([(swi[r*stepSize:(r+1)*stepSize,c*stepSize:(c+1)*stepSize]>=2).sum()
             for (r,c) in np.ndindex(nRows, nCols)], (nRows, nCols)) / stepSize**2
    tfs['HV'][-2] = tmp_tfs['HV_raw'][-2]*w1*p + tmp_tfs['HV_raw'][-2]*w2

    # save the results as a npz file
    np.savez_compressed(out_file, textureFeatures=tfs)

    if quicklook:
        # save each texture feature in a PNG
        for li in range(tfs['HH'].shape[0]):
            valid = np.isfinite(tfs['HH'][li] * tfs['HV'][li])
            for pol in ['HH', 'HV']:
                tf = tfs[pol][li]
                vmin, vmax = np.percentile(tf[valid], (1, 99))
                plt.imsave(out_file.replace('_texture_features.npz','_%s_har%02d.png' % (pol, li)),
                           tf, vmin=vmin, vmax=vmax )

    return out_file


def get_map(s1i,env):
    '''Get raster map with classification results

    Parameters
    ----------
        s1i : Sentinel1Image
            Nansat class with SAR data
        env['sigma0_min'] : list of floats
            minimum values used for scaling to gray levels
        env['sigma0_max'] : list of floats
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
    sigma0_max = env['sigma0_max']
    sigma0_min = env['sigma0_min']
    l   = env['grayLevel']    # gray-level. 32 or 64.
    ws  = env['subwindowSize']    # 1km pixel spacing (40m * 25 = 1000m)
    stp = env['stepSize']    # step size
    tfAlg = env['textureFeatureAlgorithm']
    threads = env['numberOfThreads']
    classifierFilename = env['classifierFilename']

    print('*** denoising ...')
    sigma0 = {'HH':[],'HV':[]}
    for pol in ['HH','HV']:
        s1i.add_band(array=(s1i.thermalNoiseRemoval_dev(polarization=pol, windowSize=ws)
                            / np.cos(np.deg2rad(s1i['incidence_angle']))),
                     parameters={'name': 'sigma0_%s_denoised' % pol})

    print('*** texture feature extraction ...')
    landmask = maximum_filter(s1i.landmask(skipGCP=4), ws)
    tfs = {'HH':[],'HV':[]}
    for pol in ['HH','HV']:
        grayScaleImage = convert2gray(10*np.log10(s1i['sigma0_%s_denoised' % pol]),
                                      sigma0_min[pol], sigma0_max[pol], l)
        grayScaleImage[landmask] = 0
        tfs[pol] = get_texture_features(grayScaleImage, ws, stp, threads, tfAlg)
    s1i.resize(factor=1./stp)
    for pol in ['HH','HV']:
        for li in range(13):
            s1i.add_band(array=np.squeeze(tfs[pol][li,:,:]),
                         parameters={'name': 'Haralick_%02d_%s' % (li+1, pol)})

    print('*** applying classifier ...')
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


def denoise_old(input_file, outputDirectory, unzipInput, subwindowSize, stepSize, grayLevel,
            sigma0_min, sigma0_max, quicklook, force, get_landmask):
    """ Denoise input file """
    ifilename = os.path.split(input_file)[1]
    ID = ifilename.split('.')[0]
    wdir = os.path.join(outputDirectory, ID)
    if not os.path.exists(wdir):
        os.mkdir(wdir)
    ofile = os.path.join(wdir, ID+'_sigma0.npz')
    if os.path.exists(ofile) and not force:
        print('Processed file %s already exists.' % ofile)
        return ofile

    if unzipInput:
        with zipfile.ZipFile(ifile, "r") as z:
            z.extractall()
        ifilename = ifilename[:-3]+'SAFE'
    else:
        ifilename = input_file

    results = dict()
    s1i = Sentinel1Image(ifilename)
    s1i.reproject_gcps()

    # landmask generation
    if get_landmask:
        landmask = maximum_filter(s1i.landmask(skipGCP=4).astype(np.uint8), subwindowSize)
    else:
        landmask = np.zeros(s1i.shape(), dtype=np.uint8)
    s1i.add_band(array=landmask, parameters={'name':'landmask'})

    # denoise dual-pol images
    for pol in ['HH','HV']:
        print('Denoising for %s polarization image from %s' % (pol, ifilename))
        s1i.add_band(array=s1i.texturalNoiseRemoval(polarization=pol, windowSize=subwindowSize),
                     parameters={'name':'sigma0_%s_denoised' % pol})

    # compute histograms, then apply angular dependency correction and gray level scaling
    bin_edges = np.arange(-40.0,+10.1,0.1)
    for pol in ['HH','HV']:
        # angular dependency for deformed FYI (Reference; doi: 10.1109/TGRS.2017.2721981)
        angularDependency = {'HH':-0.24, 'HV':-0.16}
        valid = (s1i['landmask']!=1)
        sigma0dB = ( 10*np.log10(s1i['sigma0_%s_denoised' % pol])
                     - (angularDependency[pol] * (s1i['incidence_angle'] - 19.)) )
        results['sigma0_%s_hist' % pol] = np.histogram(
            sigma0dB[np.isfinite(sigma0dB) * valid], bins=bin_edges )
        results['sigma0_%s' % pol] = convert2gray(sigma0dB, sigma0_min[pol], sigma0_max[pol], grayLevel)
        results['sigma0_%s' % pol][np.logical_not(valid)] = 0

    # save the results as a npz file
    np.savez_compressed(ofile, **results)

    # generate quicklook
    if quicklook:
        s1i.resize(factor=1./stepSize)
        valid = ( (s1i['landmask']!=1)
                  * np.isfinite(10*np.log10(s1i['sigma0_HH_denoised']))
                  * np.isfinite(10*np.log10(s1i['sigma0_HV_denoised'])) )
        for pol in ['HH','HV']:
            s1i.export(ofile.replace('_sigma0.npz','_sigma0_%s.tif' % pol),
                       bands=[s1i.get_band_number('sigma0_%s_denoised' % pol)], driver='GTiff')
            sigma0dB = 10*np.log10(s1i['sigma0_%s_denoised' % pol])
            vmin, vmax = np.percentile(sigma0dB[np.isfinite(sigma0dB) * valid], (1,99))
            plt.imsave( ofile.replace('_sigma0.npz','_sigma0_%s.png' % pol),
                        sigma0dB, vmin=vmin, vmax=vmax, cmap='gray' )

    # clean up
    del s1i
    if os.path.exists(ifilename) and unzipInput:
        shutil.rmtree(ifilename)

    return ofile


def denoise(input_file, outputDirectory, unzipInput, subwindowSize, stepSize, grayLevel,
            sigma0_min, sigma0_max, angularDependency, quicklook, force, get_landmask):
    """ Denoise input file """
    ifilename = os.path.split(input_file)[1]
    ID = ifilename.split('.')[0]
    wdir = os.path.join(outputDirectory, ID)
    if not os.path.exists(wdir):
        os.mkdir(wdir)
    ofile = os.path.join(wdir, ID+'_sigma0.npz')
    if os.path.exists(ofile) and not force:
        print('Processed file %s already exists.' % ofile)
        return ofile

    if unzipInput:
        with zipfile.ZipFile(ifile, "r") as z:
            z.extractall()
        ifilename = ifilename[:-3]+'SAFE'
    else:
        ifilename = input_file

    results = dict()
    s1i = Sentinel1Image(ifilename)
    s1i.reproject_gcps()

    # landmask generation
    if get_landmask:
        landmask = maximum_filter(s1i.landmask(skipGCP=4).astype(np.uint8), subwindowSize)
    else:
        landmask = np.zeros(s1i.shape(), dtype=np.uint8)
    s1i.add_band(array=landmask, parameters={'name':'landmask'})
    del landmask

    # subswath indices
    results['subswathIndices'] = s1i.subswathIndexMap('HH')

    # denoise dual-pol images
    for pol in ['HH','HV']:
        print('Denoising for %s polarization image from %s' % (pol, ifilename))
        s1i.add_band(array=s1i.rawSigma0Map(polarization=pol),
                     parameters={'name':'sigma0_%s_raw' % pol})
        s1i.add_band(array=s1i.texturalNoiseRemoval(polarization=pol, windowSize=subwindowSize),
                     parameters={'name':'sigma0_%s_denoised' % pol})

    # compute histograms, then apply angular dependency correction and gray level scaling
    bin_edges = np.arange(-40.0,+10.1,0.1)
    valid = (s1i['landmask']!=1)
    inc = s1i['incidence_angle']
    for pol in ['HH','HV']:
        for dtype in ['raw', 'denoised']:
            key = '%s_%s' % (pol, dtype)
            sigma0dB = 10*np.log10(s1i['sigma0_%s' % key]) - (angularDependency[pol] * (inc - 19.))
            results['sigma0_%s_hist' % key] = np.histogram(
                sigma0dB[np.isfinite(sigma0dB) * valid], bins=bin_edges)
            results['sigma0_%s' % key] = convert2gray(
                sigma0dB, sigma0_min[pol], sigma0_max[pol], grayLevel)
            results['sigma0_%s' % key][np.logical_not(valid)] = 0
    del valid, inc, sigma0dB

    # save the results as a npz file
    np.savez_compressed(ofile, **results)

    # generate quicklook
    if quicklook:
        s1i.resize(factor=1./stepSize)
        valid = ( (s1i['landmask']!=1)
                  * np.isfinite(10*np.log10(s1i['sigma0_HH_raw']))
                  * np.isfinite(10*np.log10(s1i['sigma0_HH_denoised']))
                  * np.isfinite(10*np.log10(s1i['sigma0_HV_raw']))
                  * np.isfinite(10*np.log10(s1i['sigma0_HV_denoised'])) )
        for pol in ['HH','HV']:
            for dtype in ['raw', 'denoised']:
                key = '%s_%s' % (pol, dtype)
                s1i.export(ofile.replace('_sigma0.npz','_sigma0_%s.tif' % key),
                           bands=[s1i.get_band_number('sigma0_%s' % key)], driver='GTiff')
                sigma0dB = 10*np.log10(s1i['sigma0_%s' % key])
                vmin, vmax = np.percentile(sigma0dB[np.isfinite(sigma0dB) * valid], (1,99))
                plt.imsave( ofile.replace('_sigma0.npz','sigma0_%s.png' % key),
                            sigma0dB, vmin=vmin, vmax=vmax, cmap='gray' )

    # clean up
    del s1i
    if os.path.exists(ifilename) and unzipInput:
        shutil.rmtree(ifilename)

    return ofile


def save_ice_map(inp_filename, raw_filename, classifier_filename, threads, source, quicklook=False, force=False):
    """ Load texture features, apply classifier and save ice map """
    # get filenames
    out_filename = inp_filename.replace('_texture_features.npz', '_classified_%s.tif' % source)
    if os.path.exists(out_filename) and not force:
        print('Processed file %s already exists.' % out_filename)
        return out_filename

    # import classifier
    plk = pickle.load(open(classifier_filename, "rb" ))
    if type(plk)==list:
        scaler, clf = plk
    else:
        class dummy_class(object):
            def transform(self, x):
                return(x)
        scaler = dummy_class()
        clf = plk
    clf.n_jobs = threads

    # get texture features
    npz = np.load(inp_filename)
    features = np.vstack([npz['textureFeatures'].item()['HH'],
                          npz['textureFeatures'].item()['HV'],
                          npz['incidenceAngle'][np.newaxis,:,:]])
    imgSize = features.shape[1:]
    features = features.reshape((27,np.prod(imgSize))).T
    gpi = np.isfinite(features.sum(axis=1))
    result = clf.predict(scaler.transform(features[gpi,:]))
    classImage = np.ones(np.prod(imgSize)) * 255
    classImage[gpi] = result
    classImage = classImage.reshape(imgSize)
    img_shape = classImage.shape

    # open original file to get geometry
    raw_nansat = Nansat(raw_filename)
    # crop and resize original Nansat to match the ice map
    raw_shape = raw_nansat.shape()
    crop = [rshape % ishape for (rshape, ishape) in zip(raw_shape, img_shape)]
    raw_nansat.crop(0,0,raw_shape[1]-crop[1], raw_shape[0]-crop[0])
    raw_nansat.resize(height=img_shape[0])
    raw_nansat.reproject_gcps()

    # create new Nansat object and add ice map
    ice_map = Nansat.from_domain(domain=raw_nansat, array=classImage.astype(np.uint8))
    ice_map.set_metadata(raw_nansat.get_metadata())
    ice_map.set_metadata('entry_title', 'S1_SAR_ICE_MAP')
    ice_map = add_colortable(ice_map)
    ice_map.export(out_filename, bands=[1], driver='GTiff')

    if quicklook:
        rgb = colorcode_array(classImage)
        plt.imsave(out_filename.replace('.tif','.png'), rgb)

    return out_filename


def colorcode_array(inp_array):
    rgb = np.zeros((inp_array.shape[0], inp_array.shape[1], 3), 'uint8')
    for k in colorDict.keys():
        rgb[inp_array==k,:] = colorDict[k]

    return rgb


def add_colortable(n_out):
    """ Add colortable to output GDAL Dataset """
    colorTable = gdal.ColorTable()
    for color in colorDict:
        colorTable.SetColorEntry(color, colorDict[color] + (255,))
    n_out.vrt.dataset.GetRasterBand(1).SetColorTable(colorTable)

    return n_out


def update_icemap_mosaic(inp_filename, inp_data, out_filename, out_domain, out_metadata):
    if os.path.exists(out_filename):
        mos_array = Nansat(out_filename)[1]
    else:
        mos_array = np.zeros(out_domain.shape(), np.uint8) + 255

    # read classification data and reproject onto mosaic domain
    n = Nansat(inp_filename)
    if inp_data is None:
        n.reproject_gcps()
        n.reproject(out_domain)
        inp_data = dict(arr=n[1], mask=n[2])

    # put data into mosaic array
    gpi = (inp_data['mask']==1) * (inp_data['arr'] < 255)
    mos_array[gpi] = inp_data['arr'][gpi]

    # export
    n_out = Nansat.from_domain(out_domain)
    n_out.add_band(array=mos_array, parameters={'name': 'classification'})
    n_out.set_metadata(n.get_metadata())
    n_out.set_metadata(out_metadata)

    n_out = add_colortable(n_out)
    n_out.export(out_filename, driver='GTiff', options=['COMPRESS=LZW'])

    return inp_data

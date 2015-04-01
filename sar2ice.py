import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
import mahotas
import pickle
from sklearn import svm

def call_haralick(subimage):
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
    haralick = mahotas.features.haralick(subimage, True)
    if haralick.shape != (4, 13):
        haralick = np.zeros((4, 13)) + np.nan
    return haralick

def clf_predict(inputData):
    ''' Apply svm on some input data
    The is used for easy pickling (needed for multiprocessing)
    '''
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
    # convert to integer leves
    iarray = 1 + l * (iarray - vmin) / (vmax - vmin)
    iarray[iarray < 1] = 1
    iarray[iarray > l] = l

    # return as unsigned integer
    return iarray.astype('uint8')

def get_texture_features(iarray, ws, stp, threads):
    ''' Calculate Haralick texture features using mahotas package

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
    harList = []
    for r in range(0, iarray.shape[0]-ws-1, stp):
        print 'Row number: ', r
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

    # convert list with texture features to array
    harImage = np.array(harList)

    # calculate directional mean
    harImageAnis = harImage.mean(axis=2)

    # reshape matrix and make images to be on the first dimension
    return np.swapaxes(harImageAnis.T, 1, 2)

def normalize_texture_features(allTF, normFile):
    ''' Log-transform, center on mean and normalize by STD each TF

    Load from prepared file vlues of log-flag, mean and STD for each TF
    Parameters
    ----------
        allTF : ndarray
            2D matrix with all texture features [num_text_feat x num_pixels]
        normFile : str
            name of file with log-flag, mean and STD
    Returns
    -------
        newTF : ndarray
            2D matrix with normalized texture features (same size, dtype)
    '''
    # load log-flag, mean and STD
    logMeanStd = np.load(normFile)

    # log-transform if needed some of the TFs
    for i, tf in enumerate(allTF):
        if logMeanStd[0, i] == 1:
            allTF[i] = np.log10(allTF[i])

    # center and normalize to STD
    allTF = (allTF - logMeanStd[1][None].T) / logMeanStd[2][None].T

    return allTF

def apply_svm(allTF, svmFile, threads):
    ''' Apply SVM to normalized texture features and lable each vector

    Parameters
    ----------
        allTF : ndarray
            2D matrix with normalized texture features [num_text_feat, num_pixes]
        svmFile : str
            name of file with pre-saved SVM
        threads : int
            number of threads for parallell computing
    Returns
    -------
        labels : ndarray
            1D vector with labels for each vector (or np.nan)
    '''

    # load SVM from pre-saved file
    clf = pickle.load(open(svmFile, "rb" ))

    # find good data for processing (not NaN)
    gpi = np.isfinite(allTF.sum(axis=0))
    allTFGood = allTF[:, gpi]

    # split good data into chunks for parallel processing
    chunkSize = 1000
    allDataGoodChunks = [allTFGood[:, i:i+chunkSize].T
                         for i in range(0, allTFGood.shape[1], chunkSize)]

    # run parallel processing of all data with SVM
    pool = Pool(threads)
    svmLablesGood = pool.map(clf_predict, allDataGoodChunks)

    # join results back from the queue and insert into full matrix
    svmLabelsGood = np.hstack(svmLablesGood)
    svmLabelsAll = np.zeros(allTF.shape[1]) + np.nan
    svmLabelsAll[gpi] = svmLabelsGood

    return svmLabelsAll

def get_map(s1i, bands, vmin, vmax,
                l=64, ws=32, stp=32, threads=2,
                normFile=None, svmFile=None):
    '''Get raster map with classification results

    Parameters
    ----------
        s1i : Sentinel1Image
            Nansat chiled with SAR data
        bands : list/tuple of strings or integers
            IDs of bands to calculate texture features from
        vmin : list/tuple of floats
            minimum values used for scaling to gray levesl
        vmax : list/tuple of floats
            maximum values used for scaling to gray levesl
        l : int
            number of gray levels
        ws : int
            sub-window size to calculate textures in
        stp : int
            step of sub-window floating
        threads : int
            number of parallell processes
        normFile : str
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
    allTF = []
    for i, bandName in enumerate(bands):
        # get array from the band
        bandArray = s1i[bandName]

        # convert to gray levels
        bandArray = convert2gray(bandArray, vmin[i], vmax[i], l)

        # mask away land
        bandArray[wm == 2] = 0

        # get texture features
        tf = get_texture_features(bandArray, ws, stp, threads)

        # append texture features as 2D matrix [13 x total_size]
        allTF.append(tf.reshape(tf.shape[0], tf.shape[1]*tf.shape[2]))

    # stack texture features from all bands into single 2D matrix
    # if two input bands only (e.g. HH and HV), size is [26 x total_size]
    allTF = np.vstack(allTF)

    # normalize texture features
    allTF = normalize_texture_features(allTF, normFile)

    # apply SVM
    lables = apply_svm(allTF, svmFile)

    # reshape vector of labels into 2D raster map
    return lables.reshape(tf.shape[1], tf.shape[2])

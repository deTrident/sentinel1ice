import os
import glob

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

"""
Join Haralick texture features from many files
Log-transform some of them
Center on mean and normalize by STD
Save normalized per input file
"""
percentile = .1


idir = '/files/sentinel1a/odata/'
normalizationName = 'norm01.npy'

ifiles = sorted(glob.glob(idir + '*HH_har.npz'))
# collect Haralick texture features and join into one matrix 26 x Number of pixels
joinedTF = []
goodFiles = []
for ifilepath in ifiles:
    hhhvTF = []
    for pol in ['HH', 'HV']:
        ifile = ifilepath.replace('HH', pol)
        if not os.path.exists(ifile):
            hhhvTF = None
        else:
            harData = np.load(ifile)['harImageAnis']
            hhhvTF.append(harData.reshape(13, harData.shape[1]*harData.shape[2]))
    if hhhvTF is not None:
        joinedTF.append(np.vstack(hhhvTF))
        goodFiles.append(ifilepath)
joinedTF = np.hstack(joinedTF)


# log-trasform TF if needed
# center and normalize
# keep log-flag, mean and std of each TF
tfLogs = []
tfStds = []
tfMins = []
tfMaxs = []
tfMeans = []
normalizedTF = []
for i, tf in enumerate(joinedTF):
    # transform to log if skewed
    tfMedian = st.nanmedian(tf)
    tfMean = np.nanmean(tf)
    tfMin = np.nanmin(tf)
    skewness = (tfMean - tfMedian) / tfMedian
    print i, skewness,
    if skewness > 0.1:
        print 'log-transform',
        tfLogs.append(True)
        newTF = np.log10(tf - tfMin + 0.1 * np.abs(tfMean))
    else:
        print 'no log-transform',
        tfLogs.append(False)
        newTF = np.array(tf)

    # get stats
    newTFStd = np.nanstd(newTF)
    newTFMean = np.nanmean(newTF)

    # center and normalize to STD
    newTF = (newTF - newTFMean) / newTFStd

    # keep Min, Max, Std and Mean
    newTFMin, newTFMax = np.percentile(newTF[np.isfinite(newTF)],
                                       (percentile, 100-percentile))
    print newTFMin, newTFMax

    tfMins.append(newTFMin)
    tfMaxs.append(newTFMax)
    tfStds.append(newTFStd)
    tfMeans.append(newTFMean)

    # clip outliers
    newTF[newTF < newTFMin] = np.nan
    newTF[newTF > newTFMax] = np.nan

    # plot histogram of normalized text feature
    plt.hist(newTF[np.isfinite(newTF)], 100)
    plt.title('%02d %f %f' % (i, newTFMin, newTFMax))
    plt.savefig(idir + 'tf_norm_hist%02d.png' % i, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close('all')

    normalizedTF.append(newTF)
normalizedTF = np.vstack(normalizedTF)


# save log, mean and std to use in operational processing
logMeanStd = np.vstack([np.array(tfLogs), np.array(tfMeans), np.array(tfStds)])
np.save(normalizationName, logMeanStd)

raise
# save normalized texture features back to input specific files
pointer = 0
for ifilepath in goodFiles:
    print 'save norm to', ifilepath
    harData = np.load(ifilepath)['harImageAnis']
    harDataSize = harData.shape[1]*harData.shape[2]
    newTFData = normalizedTF[:, pointer:pointer+harDataSize]
    pointer += harDataSize
    newTFDataHH = newTFData[:13, :].reshape(13, harData.shape[1], harData.shape[2])
    newTFDataHV = newTFData[13:, :].reshape(13, harData.shape[1], harData.shape[2])

    # remove 2 NaN neighbours
    tmp = gaussian_filter(newTFDataHH[0], 2)
    newTFDataHH[:, np.isnan(tmp)] = np.nan
    newTFDataHV[:, np.isnan(tmp)] = np.nan

    ofilehh = ifilepath.replace('HH_har', 'HH_har_norm')
    ofilehv = ifilepath.replace('HH_har', 'HV_har_norm')
    np.savez_compressed(ofilehh, newTFDataHH=newTFDataHH)
    np.savez_compressed(ofilehv, newTFDataHV=newTFDataHV)


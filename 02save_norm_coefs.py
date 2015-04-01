import os
import glob

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

"""
Join Haralick texture features from many files
Log-transform some of them
Center on mean and normalize by STD
Save normalized per input file
"""
percentile = .1
idir = '/files/sentinel1a/odata/'
normFilePrefix = 'norm01'

# independently for HH and HV
# find normalization coeeficients:
#   logFlag - should log-transform be applied ?
#   mean - offset
#   STD - scale
for pol in ['HH', 'HV']:
    # name of output file to keep normalization
    normFile = normFilePrefix + pol + '.npy'
    # input files with TFs for this pol
    ifiles = sorted(glob.glob(idir + '*%s_har.npz' % pol))
    # read TFs from many input images and keep in joinedTF
    joinedTF = []
    for ifilepath in ifiles:
        ifile = ifilepath.replace('HH', pol)
        harData = np.load(ifile)['tfs']
        joinedTF.append(harData.reshape(13, harData.shape[1]*harData.shape[2]))
    joinedTF = np.hstack(joinedTF)

    # log-trasform TF if needed
    # center and normalize
    # keep log-flag, mean and std of each TF
    tfStds = []
    tfMeans = []
    tfSkews = []
    tfOffsets = []
    for i, tf in enumerate(joinedTF):
        # transform to log if skewed
        tfMedian = st.nanmedian(tf)
        tfMean = np.nanmean(tf)
        tfMin = np.nanmin(tf)
        tfMax = np.nanmax(tf)
        tfSkew = st.skew(tf[np.isfinite(tf)])
        print pol, i, tfSkew,
        if tfSkew > 2:
            print 'log-transform',
            tfOffset = - tfMin + 0.1 * np.abs(tfMean)
            newTF = np.log10(tf + tfOffset)
        elif tfSkew < -2:
            print 'exp-transform',
            tfOffset = - tfMax
            newTF = 10 ** (tf + tfOffset)
        else:
            print 'no log-transform',
            newTF = np.array(tf)
            tfOffset = 0

        # get stats
        newTFStd = np.nanstd(newTF)
        newTFMean = np.nanmean(newTF)

        tfSkews.append(tfSkew)
        tfOffsets.append(tfOffset)
        tfStds.append(newTFStd)
        tfMeans.append(newTFMean)

        # center and normalize to STD
        newTF = (newTF - newTFMean) / newTFStd

        # plot histogram of normalized text feature
        newTFMin, newTFMax = np.percentile(newTF[np.isfinite(newTF)],
                                           (percentile, 100-percentile))
        print newTFMin, newTFMax
        plt.hist(newTF[np.isfinite(newTF)], 100)
        plt.title('%s %02d %f %f %f' % (pol, i, newTFMin, newTFMax, tfSkew))
        plt.savefig(idir + 'tf_norm_hist%s_%02d.png' % (pol, i), dpi=150, bbox_inches='tight', pad_inches=0)
        plt.close('all')

    # save log, mean and std to use in operational processing
    normCoefs = np.vstack([tfSkews, tfOffsets, tfMeans, tfStds])
    np.save(normFile, normCoefs)

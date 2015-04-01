import os
import glob

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

from sar2ice import normalize_texture_features

percentile = .1
idir = '/files/sentinel1a/odata/'
normFilePrefix = 'norm01'

# apply normalization and clipping
# load TFs, load presaved logMeanStd, normalize and save
for pol in ['HH', 'HV']:
    # name of output file to keep normalization
    normFile = normFilePrefix + pol + '.npy'
    # input files with TFs for this pol
    ifiles = sorted(glob.glob(idir + '*%s_har.npz' % pol))
    for ifile in ifiles:
        # read TFs from HH or HV and keep in hhhvTF
        tfs = np.load(ifile)['tfs']
        tfsNorm = normalize_texture_features(tfs, normFile)

        # get min, max from histogram and clip
        for i, tf in enumerate(tfsNorm):
            if len(tf[np.isfinite(tf)]) == 0:
                continue
            tfMin, tfMax = np.percentile(tf[np.isfinite(tf)],
                                           (percentile, 100-percentile))
            # clip outliers
            tfsNorm[i, tf < tfMin] = np.nan
            tfsNorm[i, tf > tfMax] = np.nan

            # remove 2 NaN neighbours
            tfGaus = gaussian_filter(tfsNorm[i], 1)
            tfsNorm[i, np.isnan(tfGaus)] = np.nan

        # save to output file
        ofile = ifile.replace('_har', '_har_norm')
        np.savez_compressed(ofile, tfsNorm=tfsNorm)

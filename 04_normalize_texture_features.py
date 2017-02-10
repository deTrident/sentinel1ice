''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from sar2ice import normalize_texture_features
from config import get_env


idir = get_env()['outputDirectory']
normFilePrefix = get_env()['textureFeatureNormalizationFilePrefix']
trans_thres = get_env()['skewnessThreshold']
percentile = 0     # caution: clipping results in more void cells.
gaus_size = 0.2 # c.a. 3 pixels

# apply normalization and clipping
# load TFs, load presaved logMeanStd, normalize and save

for pol in ['HH', 'HV']:
    
    normFile = normFilePrefix+pol+'.npz'
    ifiles = sorted(glob.glob(idir+'*/*%s_har.npz' % pol))
    
    for ifile in ifiles:
        
        print('Texture features normalization of %s' %os.path.split(ifile)[1])
        tfs = np.load(ifile)['tfs']
        tfsNorm = normalize_texture_features(
            tfs, normFile, skew_thres=trans_thres )

        # get min, max from histogram and clip
        for i, tf in enumerate(tfsNorm):
            if len(tf[np.isfinite(tf)]) == 0:
                continue
            tfMin, tfMax = np.percentile(
                tf[np.isfinite(tf)], (percentile, 100-percentile) )
            # replace outliers with max/min. clipping results in void cells.
            tfsNorm[i, tf < tfMin] = tfMin
            tfsNorm[i, tf > tfMax] = tfMax
            # remove 2 NaN neighbours
            tfGaus = gaussian_filter(tfsNorm[i], gaus_size)
            tfsNorm[i, np.isnan(tfGaus)] = np.nan
        
        # save each normalized texture feature in a PNG
        for i, tf in enumerate(tfsNorm):
            vmin, vmax = np.percentile( tf[np.isfinite(tf)], (2.5, 97.5) )
            plt.imsave( ifile.replace('har.npz','har%02d_norm.png' % i),
                        tf, vmin=vmin, vmax=vmax )
        
        # save normalized texture features to output file
        proc_params = np.load(ifile)['proc_params']
        np.savez_compressed( ifile.replace('_har.npz','_har_norm.npz'),
                             tfsNorm=tfsNorm, proc_params=proc_params )

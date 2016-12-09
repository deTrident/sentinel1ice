import os, glob
import numpy as np
from scipy.ndimage.filters import gaussian_filter

from sar2ice import normalize_texture_features, normalize_texture_features

idir = ( os.path.abspath(os.getcwd()+'/../shared/test_data/sentinel1a_l1')
        + '/odata_FramStrait_TFs/' )
normFilePrefix = 'norm01'
trans_thres = 0.
trans_alg = 'boxcox'
percentile = .1
gaus_size = 0.2 # c.a. 3 pixels

# apply normalization and clipping
# load TFs, load presaved logMeanStd, normalize and save

for pol in ['HH', 'HV']:
    
    normFile = os.path.join(idir, normFilePrefix + pol + '.npy')
    ifiles = sorted(glob.glob(idir + '*%s_har.npz' % pol))
    
    for ifile in ifiles:
        
        print('Texture features normalization of %s' %os.path.split(ifile)[1])
        tfs = np.load(ifile)['tfs']
        tfsNorm = normalize_texture_features(
            tfs, normFile, algorithm=trans_alg, skew_thres=trans_thres )

        # get min, max from histogram and clip
        for i, tf in enumerate(tfsNorm):
            if len(tf[np.isfinite(tf)]) == 0:
                continue
            tfMin, tfMax = np.percentile(
                tf[np.isfinite(tf)], (percentile, 100-percentile) )
            # clip outliers
            tf[np.isnan(tf)] = tfMin-np.finfo(tf.dtype).eps
            tfsNorm[i, tf < tfMin] = np.nan
            tf[np.isnan(tf)] = tfMax-np.finfo(tf.dtype).eps
            tfsNorm[i, tf > tfMax] = np.nan
            # remove 2 NaN neighbours
            tfGaus = gaussian_filter(tfsNorm[i], gaus_size)
            tfsNorm[i, np.isnan(tfGaus)] = np.nan

        # save each normalized texture feature in a PNG
        for i, tf in enumerate(tfsNorm):
            vmin = np.percentile( tf[np.isfinite(tf)], 2.5 )
            vmax = np.percentile( tf[np.isfinite(tf)], 97.5 )
            plt.imsave( ifile.replace('har.npz','har%02d_norm.png' % i),
                        tf, vmin=vmin, vmax=vmax )

        # save normalized texture features to output file
        proc_params = np.load(ifile)['proc_params']
        np.savez_compressed( ifile.replace('_har.npz','_har_norm.npz'),
                             tfsNorm=tfsNorm, proc_params=proc_params )

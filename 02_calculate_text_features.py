### CALCULATE HARALICK TEXTURE FEATURES.

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sar2ice import get_texture_features
from config import get_env

# read configuration
env = get_env()
# set up parameters for Haralick texture features computation
stp = env['stepSize']    # step size
ws  = env['subwindowSize']    # 1km pixel spacing (40m * 25 = 1000m)
threads = env['numberOfThreads']
alg = env['textureFeatureAlgorithm']
idir = env['outputDirectory']
# listup denoised image files
ifiles = sorted(glob.glob(idir + '*/S1?_EW_GRDM_1SDH*_gamma0.npz'))
# process each file
for ifile in ifiles:
    ifilename = os.path.split(ifile)[1]
    ofile = ifile.replace('_gamma0','_texture_features')
    print(ifilename)
    if os.path.exists(ofile):
        print('Processed data file already exists.')
        continue
    npz = np.load(ifile)
    tfs = {}
    for pol in ['HH', 'HV']:
        print('Computing texture features for %s polarization.' % pol)
        # get texture features
        tfs[pol] = get_texture_features(npz['gamma0_%s' % pol], ws, stp, threads, alg)
        # save each texture feature in a PNG
        for i, tf in enumerate(tfs[pol]):
            vmin, vmax = np.percentile( tf[np.isfinite(tf)], (2.5, 97.5) )
            plt.imsave( ofile.replace('_texture_features.npz','_%s_har%02d.png' % (pol, i)),
                        tf, vmin=vmin, vmax=vmax )
    # save the results as a npz file
    np.savez_compressed( ofile, textureFeatures=tfs, incidenceAngle=npz['incidenceAngle'])

### CALCULATE HARALICK TEXTURE FEATURES.

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sar2ice import get_texture_features
import config as cfg

# listup denoised image files
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/S1?_EW_GRDM_1SDH*_gamma0.npz'))
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
        tfs[pol] = get_texture_features(npz['gamma0_%s' % pol], cfg.subwindowSize, cfg.stepSize, cfg.numberOfThreads, cfg.textureFeatureAlgorithm)
        # save each texture feature in a PNG
        for i, tf in enumerate(tfs[pol]):
            vmin, vmax = np.percentile( tf[np.isfinite(tf)], (2.5, 97.5) )
            plt.imsave( ofile.replace('_texture_features.npz','_%s_har%02d.png' % (pol, i)),
                        tf, vmin=vmin, vmax=vmax )
    # save the results as a npz file
    np.savez_compressed( ofile, textureFeatures=tfs, incidenceAngle=npz['incidenceAngle'])

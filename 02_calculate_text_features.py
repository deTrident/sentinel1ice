### CALCULATE HARALICK TEXTURE FEATURES.

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sar2ice import save_texture_features
import config as cfg

# listup denoised image files
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/S1?_EW_GRDM_1SDH*_gamma0.npz'))
# process each file
for ifile in ifiles:
    out_file = save_texture_features(ifile, cfg.subwindowSize, cfg.stepSize, cfg.numberOfThreads,
                                            cfg.textureFeatureAlgorithm, cfg.quicklook, cfg.force)

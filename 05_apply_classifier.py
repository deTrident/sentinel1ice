### APPLY CLASSIFIER TO THE PRE-COMPUTED TEXTURE FEATURES

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, pickle
import numpy as np
from nansat import Nansat
from sar2ice import colorDict

import config as cfg


# listup texture feature files
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/S1?_EW_GRDM_1SDH*_texture_features.npz'))
# process each file
for ifile in ifiles:

    nansat_filename = ifile.replace('_texture_features.npz','_denoised_gamma0_HH.tif')
    if not os.path.exists(nansat_filename):
        nansat_filename = glob.glob(cfg.inputDirectory + os.path.basename(ifile).replace('_texture_features.npz', '*'))[0]

    out_filename = save_ice_map(ifile, nansat_filename, cfg.classifierFilename,
                                                        cfg.numberOfThreads,
                                                        cfg.sourceType,
                                                        cfg.quicklook)

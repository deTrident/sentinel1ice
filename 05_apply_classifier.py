### APPLY CLASSIFIER TO THE PRE-COMPUTED TEXTURE FEATURES

import os, glob
from sar2ice import save_ice_map
import config as cfg


# listup texture feature files
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/S1?_EW_GRDM_1SDH*_texture_features.npz'))
# process each file
for ifile in ifiles:
    nansat_filename = ifile.replace('_texture_features.npz','_sigma0_HH_denoised.tif')
    if not os.path.exists(nansat_filename):
        nansat_filename = glob.glob(cfg.inputDirectory
                              + os.path.basename(ifile).replace('_texture_features.npz', '*'))[0]
    out_filename = save_ice_map(ifile, nansat_filename, cfg.classifierFilename, cfg.numberOfThreads,
                                cfg.sourceType, cfg.quicklook, cfg.force)
    print(out_filename)

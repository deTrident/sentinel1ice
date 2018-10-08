### CALCULATE HARALICK TEXTURE FEATURES.

import os, glob
from sar2ice import save_texture_features
import config as cfg

# listup denoised image files
ifiles = sorted(glob.glob(os.path.join(cfg.outputDirectory,cfg.wildcard,'*_sigma0.npz')))
# process each file
for ifile in ifiles:
    out_file = save_texture_features(ifile, cfg.subwindowSize, cfg.stepSize, cfg.numberOfThreads,
                                     cfg.textureFeatureAlgorithm, cfg.quicklook, cfg.force)

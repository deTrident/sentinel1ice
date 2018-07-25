### DENOISE HH/HV IMAGES AND SAVE THEM WITH SOME OF THEIR CORRESPONDNIG ATTRIBUTES.
### USE THIS IF THE COMPUTATIONAL RESOURCES ARE ENOUGH TO RUN PARALLEL PROCESSING.

import importlib
import os, glob
from multiprocessing import Pool

from sar2ice import denoise
import config as cfg
importlib.reload(cfg)


shared_args = None
def denoise_mp(input_file):
    """ Wrapper for denoise() to be used in multiprocessing"""
    global shared_args
    denoise(input_file, *shared_args)

def _init_pool(*args):
    """ Initialize shared data for multiprocessing """
    global shared_args
    shared_args = args

# find input files
ifiles = sorted(glob.glob(cfg.inputDirectory + cfg.wildcard), reverse=True)
if (cfg.minDate!=None) and (cfg.maxDate!=None):
    ifiles = [ifile for ifile in ifiles if minDate <= os.path.split(ifile)[-1][17:25] <= maxDate]

if cfg.numberOfThreads == 0:
    # run denosing without threads
    for ifile in ifiles:
        denoise(ifile, cfg.outputDirectory, cfg.unzipInput, cfg.subwindowSize, cfg.stepSize, cfg.grayLevel, cfg.gamma0_min, cfg.gamma0_max, cfg.quicklook)
else:
    # run denosing in multiple threads
    p = Pool(cfg.numberOfThreads, initializer=_init_pool,
             initargs=(cfg.outputDirectory, cfg.unzipInput, cfg.subwindowSize, cfg.stepSize, cfg.grayLevel, cfg.gamma0_min, cfg.gamma0_max, cfg.quicklook))
    results = p.map(denoise_mp, ifiles)
    p.close()
    p.terminate()
    p.join()
    del p


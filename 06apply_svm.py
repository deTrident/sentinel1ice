import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
import mahotas

from sentinel1image import Sentinel1Image
from sar2ice import get_map



# find input files
idir = '/files/sentinel1a/'
odir = '/files/sentinel1a/odata/'
ifiles = sorted(glob.glob(idir + '*.SAFE'))
bands = ['sigma0_HH', 'sigma0_HV']
vmin = [-15, -26]
vmax = [0,   -14]
stp = 16
ws  = 32
l   = 64
threads = 6
normFiles = ['norm01HH.npy', 'norm01HH.npy']
svmFile = 'svm.pickle'

for ifile in ifiles:
    s2i = Sentinel1Image(ifile)
    iceMask = get_map(s2i, bands, vmin, vmax,
                    l, ws, stp, threads,
                    normFiles, svmFile)
    plt.imsave(ifile + '_svm_zones_hires.png')

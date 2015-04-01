import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
import mahotas

from sentinel1image import Sentinel1Image
from sar2ice import SAR2Ice


class Sentinel2Ice(Sentinel1Image, SAR2Ice):
    pass


# find input files
idir = '/files/sentinel1a/'
odir = '/files/sentinel1a/odata/'
ifiles = sorted(glob.glob(idir + '*.SAFE'))

s2i = Sentinel2Ice(ifiles[0])

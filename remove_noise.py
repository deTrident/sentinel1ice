import os
import glob

import numpy as np
import scipy.stats as st
import scipy.interpolate as sp

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from nansat import *
from sentinel1image import Sentinel1Image

# remove thermal noise and anglura dependence from sigma0 in HH and HV of
# several scence

# min/max of sigma0 for non-corr and corrected values
vmax = {'HH' : [-5, -5], 'HV' : [-18, -17]}
vmin = {'HH' : [-25, -12], 'HV' : [-33, -23]}


resizeFactor = 0.1


idir = '/files/sentinel1a/'
s1afiles = sorted(glob.glob(idir + '*.SAFE'))
odir = '/files/sentinel1a/'

# remove thermal noise and anglura dependence from sigma0 in HH and HV of
# several scence

# min/max of sigma0 for non-corr and corrected values
vmax = {'HH' : [-5, -5], 'HV' : [-18, -17]}
vmin = {'HH' : [-25, -12], 'HV' : [-33, -23]}


resizeFactor = 0.1

idir = '/files/sentinel1a/'
s1afiles = sorted(glob.glob(idir + '*.SAFE'))
odir = '/files/sentinel1a/'

for s1afile in s1afiles:
    print s1afile
    ofile = os.path.join(odir, os.path.splitext(os.path.split(s1afile)[1])[0])
    n = Sentinel1Image(s1afile)
    print 'open - OK'
    n.resize(resizeFactor, eResampleAlg=0) # nearest neighbour, just for test

    for pol in ['HH', 'HV']:
        n.write_figure(ofile + 'sigma0_%scor.jpg' % pol,
                       'sigma0_%s' % pol,
                       clim='hist', cmapName='gray')
        raise
    del n

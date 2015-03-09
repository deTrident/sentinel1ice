import os
import glob
from multiprocessing import Pool

import numpy as np
import scipy.stats as st
import scipy.interpolate as sp
from django.contrib.gis.geos import Polygon

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from nansat import *
from sentinel1image import Sentinel1Image

import os, sys
print sys.path.append('/home/vagrant/py/nansen-cloud/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nansencloud.settings")
import django
django.setup()

from cat.models import Image

# remove thermal noise and anglura dependence from sigma0 in HH and HV of
# several scences

def write_sigma0_figure(ifile):
    print ifile
    ofile = os.path.join(odir, os.path.splitext(os.path.split(ifile)[1])[0])
    n = Sentinel1Image(ifile)
    print 'open - OK'
    n.resize(resizeFactor, eResampleAlg=0) # nearest neighbour, just for test

    for pol in ['HH', 'HV']:
        sigma0 = 10 * np.log10(n['sigma0_%s' % pol])
        f = Figure(sigma0)
        f.process(cmin=vmin[pol][1], cmax=vmax[pol][1], cmapName='gray')
        f.save(ofile + 'sigma0_%scor.jpg' % pol)
        del f
        del sigma0

# min/max of sigma0 for non-corr and corrected values
vmax = {'HH' : [-5, -5], 'HV' : [-18, -17]}
vmin = {'HH' : [-25, -12], 'HV' : [-33, -23]}

resizeFactor = 0.1

odir = '/files/sentinel1a/'

p = Polygon(((-5, 78), (-4, 78), (-4, 79), (-5, 79), (-5, 78)))
images = Image.objects.filter(border__intersects=p).filter(sourcefile__name__startswith='S1A_EW_GRDM_1SDH')
print len(images)


pool = Pool(4)
pool.map(write_sigma0_figure, sorted(images.sourcefiles()))

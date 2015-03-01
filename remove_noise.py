import os
import glob

import numpy as np
import scipy.stats as st
import scipy.interpolate as sp

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from nansat import *

# remove thermal noise and anglura dependence from sigma0 in HH and HV of
# several scence

# min/max of sigma0 for non-corr and corrected values
vmax = {'HH' : [-5, -5], 'HV' : [-18, -17]}
vmin = {'HH' : [-25, -12], 'HV' : [-33, -23]}


resizeFactor = 0.1


idir = '/files/sentinel1a/'
s1afiles = sorted(glob.glob(idir + '*.SAFE'))
odir = '/files/sentinel1a/'

clims = {'HH': [], 'HV': []}

for s1afile in s1afiles:
    print s1afile
    ofile = os.path.join(odir, os.path.splitext(os.path.split(s1afile)[1])[0])
    n = Nansat(s1afile)
    print 'open - OK'
    n.resize(resizeFactor, eResampleAlg=0) # nearest neighbour, just for test
    # load data from file
    eaMatrix = n['elevation_angle']

    for pol in ['HH', 'HV']:
        sigma0 = n['sigma0_%s' % pol]
        f = Figure(10 * np.log10(sigma0))
        cmin, cmax = f.clim_from_histogram(ratio=0.95)
        f.process(cmin=vmin[pol][0], cmax=vmax[pol][0], cmapName='gray')
        f.save(ofile + 'sigma0_%s.jpg' % pol)

        # load noise from file
        s1aNoise = np.load('s1a_%s_thermal_noise.npz' % pol)
        noiseArrays = [s1aNoise[noiseFile] for noiseFile in sorted(s1aNoise.files)]

        # find minimum noise
        maxNoise = 0
        for noiseArray in noiseArrays:
            maxNoise = max(maxNoise, max(noiseArray[1]))
            print maxNoise

        # subtract maximum noise from other noise values
        for noiseArray in noiseArrays:
            noiseArray[1] -= maxNoise


        noiseMatrix = np.zeros_like(eaMatrix) + np.nan
        for noiseArray in noiseArrays:
            minEA = np.nanmin(noiseArray[0])
            maxEA = np.nanmax(noiseArray[0])
            print minEA, maxEA

            # train interpolator
            fc = sp.InterpolatedUnivariateSpline(noiseArray[0], noiseArray[1], k=3)

            # calculate noise
            swathMask = (eaMatrix >= minEA) * (eaMatrix <= maxEA)
            noiseMatrix[swathMask] = fc(eaMatrix[swathMask])

        del swathMask

        sigma0 = sigma0 - noiseMatrix
        del noiseMatrix

        f = Figure(10 * np.log10(sigma0))
        f.process(cmin=vmin[pol][1], cmax=vmax[pol][1], cmapName='gray')
        f.save(ofile + 'sigma0_%scor.jpg' % pol)
        del sigma0


    del eaMatrix
    del n

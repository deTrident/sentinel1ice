import os
import glob

import numpy as np
import scipy.stats as st
import scipy.interpolate as sp

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from nansat import *

vmax = {'HH' : -5, 'HV' : -22}
vmin = {'HH' : -20, 'HV' : -38}

resizeFactor = 0.1

s1afiles = glob.glob('*.SAFE')
for s1afile in s1afiles:
    print s1afile
    ofile = os.path.splitext(s1afile)[0]
    n = Nansat(s1afile)
    print 'open - OK'
    n.resize(resizeFactor, eResampleAlg=0)
    # load data from file
    eaMatrix = n['elevation_angle']

    for pol in ['HH', 'HV']:
        sigma0 = n['sigma0_%s' % pol]
        plt.imsave(ofile + 'sigma0_%s.jpg' % pol, 10 * np.log10(sigma0), vmin=vmin[pol], vmax=vmax[pol], cmap='gray')

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

        plt.imsave(ofile + 'sigma0_%scor.jpg' % pol, 10 * np.log10(sigma0), vmin=vmin[pol]+7, vmax=vmax[pol]+7, cmap='gray')
        del sigma0


    del eaMatrix
    del n

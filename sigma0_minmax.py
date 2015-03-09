import os
import inspect
import glob

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sp
from matplotlib.colors import LogNorm

pol = 'HV'
idir = '/files/sentinel1a/'

ifiles = sorted(glob.glob(idir + 'S1A_EW_GRDM_1SDH_*.zip_%s_stats.npz' % pol))

goodEAs = []
goodMins = []
goodMaxs = []

for ifile in ifiles:
    print ifile
    inpEA = np.load(ifile)['sigma0_%s_stats' % pol][0]
    inpStd = np.load(ifile)['sigma0_%s_stats' % pol][1]
    inpMean = np.load(ifile)['sigma0_%s_stats' % pol][2]


    # load presaved thermal noise estimates
    selfDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    s1aNoise = np.load(os.path.join(selfDir, 's1a_%s_thermal_noise.npz' % pol))
    noiseArrays = [s1aNoise[noiseFile] for noiseFile in sorted(s1aNoise.files)]

    # find maximum noise
    maxNoise = 0
    for noiseArray in noiseArrays:
        maxNoise = max(maxNoise, max(noiseArray[1]))

    # subtract maximum noise from other noise values
    for noiseArray in noiseArrays:
        noiseArray[1] -= maxNoise

    inpMin = np.zeros_like(inpMean) + np.nan
    inpMax = np.zeros_like(inpMean) + np.nan
    for noiseArray in noiseArrays:
        minEA = np.nanmin(noiseArray[0])
        maxEA = np.nanmax(noiseArray[0])

        # train interpolator
        fc = sp.InterpolatedUnivariateSpline(noiseArray[0], noiseArray[1], k=3)

        swathMask = (inpEA >= minEA) * (inpEA <= maxEA)
        noiseValues = fc(inpEA[swathMask])
        inpMin[swathMask] = 10 ** ((inpMean[swathMask] - inpStd[swathMask] * 3) / 10) - noiseValues
        inpMax[swathMask] = 10 ** ((inpMean[swathMask] + inpStd[swathMask] * 3) / 10) - noiseValues

    goodEAs.append(inpEA[np.isfinite(inpMin)])
    goodMins.append(inpMin[np.isfinite(inpMin)])
    goodMaxs.append(inpMax[np.isfinite(inpMin)])

#plt.plot(inpEA, inpMin, '.', inpEA, inpMax, '.')
goodEAs = np.hstack(goodEAs)
minEA = np.nanmin(goodEAs)
maxEA = np.nanmax(goodEAs)

goodMins = 10 * np.log10(np.hstack(goodMins))
goodMaxs = 10 * np.log10(np.hstack(goodMaxs))

bins = 200
dmin = 1
dmax = 10
s0MinMin = -35
s0MinMax = +05

s0MaxMin = -35
s0MaxMax = +05

tmp = plt.subplot(221)
plt.hist2d(goodEAs, goodMins, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [s0MinMin, s0MinMax]])

tmp = plt.subplot(222)
plt.hist2d(goodEAs, goodMaxs, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [s0MaxMin, s0MaxMax]])

tmp = plt.subplot(223)
plt.hist(goodMins, bins)

tmp = plt.subplot(224)
plt.hist(goodMaxs, bins)

plt.savefig('sigma0minmax_%s.png' % pol, dpi=300)
plt.show()

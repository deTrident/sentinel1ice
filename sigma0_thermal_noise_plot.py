import os
import inspect
import glob

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sp
from matplotlib.colors import LogNorm

pol = 'HH'
idir = '/files/sentinel1a/'

ifiles = sorted(glob.glob(idir + 'S1A_EW_GRDM_1SDH_*.zip_%s_stats.npz' % pol))

goodEAs = []
goodMeans = []
goodMeansCor = []

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

    inpMeanCor = np.zeros_like(inpMean) + np.nan
    noiseMed = []
    eaMed = []
    for noiseArray in noiseArrays:
        noiseMed.append(noiseArray[1] + maxNoise)
        eaMed.append(noiseArray[0])
        minEA = np.nanmin(noiseArray[0])
        maxEA = np.nanmax(noiseArray[0])

        # train interpolator
        fc = sp.InterpolatedUnivariateSpline(noiseArray[0], noiseArray[1], k=3)

        swathMask = (inpEA >= minEA) * (inpEA <= maxEA)
        noiseValues = fc(inpEA[swathMask])
        inpMeanCor[swathMask] = 10 ** (inpMean[swathMask] / 10) - noiseValues

    goodEAs.append(inpEA[np.isfinite(inpMeanCor)])
    goodMeans.append(inpMean[np.isfinite(inpMeanCor)])
    goodMeansCor.append(inpMeanCor[np.isfinite(inpMeanCor)])

#plt.plot(inpEA, inpMin, '.', inpEA, inpMax, '.')
goodEAs = np.hstack(goodEAs)
minEA = np.nanmin(goodEAs)
maxEA = np.nanmax(goodEAs)

goodMeans = np.hstack(goodMeans)
goodMeansCor = 10 * np.log10(np.hstack(goodMeansCor))

noiseMed = 10 * np.log10(np.hstack(noiseMed))
eaMed = np.hstack(eaMed)

bins = 200
dmin = 1
dmax = 100
# HH
s0Min = -20
s0Max = -05
# HV
#s0Min = -35
#s0Max = -15

f = plt.Figure(figsize=(3,3))
ax1 = plt.subplot(311)
plt.hist2d(goodEAs, goodMeans, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [s0Min, s0Max]])
ax1.set_ylabel('Original\nsigma0_%s, dB' % pol)
ax1.set_xlabel('Elevation angle')

ax2 = plt.subplot(312, sharex=ax1)
plt.plot(eaMed, noiseMed, 'k.-')
ax2.set_ylabel('Thermal noise\nin sigma0_%s, dB' % pol)

ax3 = plt.subplot(313, sharex=ax1)
plt.hist2d(goodEAs, goodMeansCor, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [s0Min, s0Max]])
ax3.set_ylabel('Corrected\nsigma0_%s, dB' % pol)

plt.suptitle('Correction of thermal noise of sigma0_%s' % pol)
plt.savefig('sigma0_%s_correction.png' % pol, dpi=300)
plt.show()

import os
import glob

import numpy as np
import scipy.stats as st
import scipy.interpolate as sp

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

polarization = 'HH'

ifiles = glob.glob('/files/sentinel1a/S1A*.zip_%s_stats.npz' % polarization)

meanStds = []
stds = []
eas = []
means = []

goodEAs = []
goodSTDs = []
goodMeans = []
goodAnomalies = []

swathsHV = {
    1: {
        'minEA': 17.40,
        'maxEA': 25.45,
        'maxMeanStd': {'HV' : 0.00015, 'HH': 0.01},
    },
    2: {
        'minEA': 25.53,
        'maxEA': 30.00,
        'maxMeanStd': {'HV': 0.0001, 'HH': 0.01},
    },
    3: {
        'minEA': 30.00,
        'maxEA': 34.52,
        'maxMeanStd': {'HV': 0.0001, 'HH': 0.007},
    },
    4: {
        'minEA': 34.58,
        'maxEA': 38.06,
        'maxMeanStd': {'HV': 0.00007, 'HH': 0.007},
    },
    5: {
        'minEA': 38.13,
        'maxEA': 40.60,
        'maxMeanStd': {'HV': 0.00007, 'HH': 0.007},
    }
}

swathsHH = {
    0: {
        'minEA': 17.40,
        'maxEA': 40.50,
        'maxMeanStd': {'HV': 0.00007, 'HH': 0.01},
    }
}

swaths = {'HH': swathsHH, 'HV':swathsHV}[polarization]

dEA = {'HH': 0.5, 'HV': 0.05} # each pixel is ca 0.002 deg

swathData = []

for swath in swaths:
    print swath
    minEA = swaths[swath]['minEA']
    maxEA = swaths[swath]['maxEA']
    maxMeanStd = swaths[swath]['maxMeanStd'][polarization]

    for ifile in ifiles:
        sigma0_stats = np.load(ifile)['sigma0_%s_stats' % polarization]

        ea = sigma0_stats[0]
        s0std = sigma0_stats[1]
        s0mean = sigma0_stats[2]

        # convert back to linear units
        s0var = np.abs(s0std / s0mean)     # variance
        s0mean = 10 ** (s0mean / 10)
        s0std = s0var * s0mean

        gpi = (np.isfinite(ea) *
               np.isfinite(s0std) *
               np.isfinite(s0mean) *
               (ea > minEA) *
               (ea < maxEA))

        eas = np.hstack((eas, ea[gpi]))
        stds = np.hstack((stds, s0std[gpi]))
        means = np.hstack((means, s0mean[gpi]))
        meanStd = np.mean(s0std[gpi])

        if np.isfinite(meanStd) and meanStd < maxMeanStd:
            goodEAs = np.hstack((goodEAs, ea[gpi]))
            goodSTDs = np.hstack((goodSTDs, s0std[gpi]))
            goodMeans = np.hstack((goodMeans, s0mean[gpi]))

        print len(gpi[gpi])
        if len(gpi[gpi]) == 0:
            print 'Remove %s ' % ifile
            os.remove(ifile)
        else:
            meanStds.append(meanStd)

    bins = 200
    dmin = 1
    dmax = 200
    tmp = plt.subplot(321)

    s0MeanMax1 = {'HH': 0.4, 'HV': 0.010}[polarization]
    s0MeanMax2 = {'HH': 0.3, 'HV': 0.005}[polarization]
    s0StdMax1 = {'HH': 0.4,  'HV': 0.002}[polarization]
    s0StdMax2 = {'HH': 0.02,  'HV': 0.001}[polarization]


    tmp = plt.hist2d(eas, means, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [0, s0MeanMax1]])

    tmp = plt.subplot(322)
    tmp = plt.hist2d(eas, stds, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [0, s0StdMax1]])


    tmp = plt.subplot(323)
    tmp = plt.hist2d(goodEAs, goodMeans, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [0, s0MeanMax2]])

    # estimated noise
    noiseEstim = goodMeans

    # simulated pixels
    pixSize = dEA[polarization]
    simPixels = (maxEA - minEA) / pixSize
    print 'simPixels = ', simPixels
    eaSim = np.linspace(minEA, maxEA + pixSize + pixSize, simPixels)

    # MEDIAN for each simulated pixel
    noiseMed = []
    for i, ea in enumerate(eaSim[:-1]):
        noiseMed.append(st.nanmedian(noiseEstim[(goodEAs > eaSim[i]) * (goodEAs < eaSim[i+1])]))

    # kepp only not NAN
    noiseMed = np.array(noiseMed)
    gpi = np.isfinite(noiseMed)
    eaSim = eaSim[:-1][gpi]
    noiseMed = noiseMed[gpi]


    plt.plot(eaSim, noiseMed, '.-k')
    plt.savefig('swath_%s_%02d.png' % (polarization, swath), dpi=300)
    print 'OK!'


    tmp = plt.subplot(324)
    tmp = plt.hist2d(goodEAs, goodSTDs, (bins, bins), norm=LogNorm(vmin=dmin, vmax=dmax), range=[[minEA, maxEA], [0, s0StdMax2]])


    tmp = plt.subplot(325)
    tmp = plt.hist(meanStds, 100)

    plt.show()
    plt.close()
    thermalNoiseData = np.vstack((eaSim, noiseMed))
    swathData.append(thermalNoiseData)

# save median noise values
np.savez('s1a_%s_thermal_noise.npz' % polarization, swathData[0]) # in case of single swath...
np.savez('s1a_%s_thermal_noise.npz' % polarization,
         swathData[0],
         swathData[1],
         swathData[2],
         swathData[3],
         swathData[4])


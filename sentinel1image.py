import os
import inspect

import numpy as np
import scipy.interpolate as sp

from nansat import Nansat

class Sentinel1Image(Nansat):
    ''' Apply angular correction and noise removeal to Sentinel1a SAR data '''

    def __getitem__(self, bandID):
        ''' Returns sigma0 corrected for thermal noise '''
        # get band, name and data
        band = self.get_GDALRasterBand(bandID)
        name = band.GetMetadata().get('name', '')
        dataArray = Nansat.__getitem__(self, bandID)

        # return original data from other bands
        if name not in ['sigma0_HH', 'sigma0_HV']:
            return dataArray

        # get polarization
        pol = name[-2:]

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

        # get elevation angle and original sigma0 from Nansat
        eaMatrix = self['elevation_angle']

        clearDataArray = np.zeros_like(dataArray) + np.nan
        # create noise matrix and fill with noise for eah swath
        for noiseArray in noiseArrays:
            minEA = np.nanmin(noiseArray[0])
            maxEA = np.nanmax(noiseArray[0])

            # train interpolator
            fc = sp.InterpolatedUnivariateSpline(noiseArray[0], noiseArray[1], k=3)

            # calculate noise
            swathMask = (eaMatrix >= minEA) * (eaMatrix <= maxEA)
            noiseValues = fc(eaMatrix[swathMask])

            clearDataArray[swathMask] = dataArray[swathMask] - noiseValues
            # free mem
            del noiseValues
            del swathMask

        del eaMatrix

        # return data in decibels
        return 10 * np.log10(clearDataArray)

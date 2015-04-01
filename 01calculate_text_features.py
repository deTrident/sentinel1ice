import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
import mahotas

from sentinel1image import Sentinel1Image
from sar2ice import convert2gray, get_texture_features

# find input files
idir = '/files/sentinel1a/'
odir = '/files/sentinel1a/odata/'
ifiles = sorted(glob.glob(idir + '*.SAFE'))

## set up parameters for Haralick texture features computation
stp = 32
ws  = 32
l   = 64
sigma0_max = {'HH': 0,   'HV': -14}
sigma0_min = {'HH': -15, 'HV': -26}
threads = 6

for ifilepath in ifiles:
    ifile = os.path.split(ifilepath)[1]
    print ifile
    for pol in ['HH', 'HV']:
        # set output file namew
        ofile = '%s_%s_' % (os.path.join(odir, ifile), pol)
        ofileNPZ = ofile + 'har.npz'

        # skip processing already extisting files
        if os.path.exists(ofileNPZ):
            continue

        # read data from input file
        s1i = Sentinel1Image(idir + ifile)
        #s1i.crop(2000, 2000, 1000, 1000)  # for testing only
        print 'Read sigma0_%s from %s' % (pol, ifile)
        sigma0 = s1i['sigma0_%s' % pol]

        # make full res JPG
        plt.imsave(ofile + 'sigma0.jpg', sigma0, vmin=sigma0_min[pol], vmax=sigma0_max[pol], cmap='gray')

        # convert to integer leves
        sigma0 = convert2gray(sigma0, sigma0_min[pol], sigma0_max[pol], l)

        # mask land
        print 'mask land'
        wm = s1i.watermask()[1]
        sigma0[wm == 2] = 0

        # get texture features
        tfs = get_texture_features(sigma0, ws, stp, threads)

        # save each texture feature in a PNG
        for i, tf in enumerate(tfs):
            plt.imsave(ofile + 'har%02d.png' % i, tf)

        # save texture features for further processing (
        #     unsupervised classification,
        #     teaching SVM
        #     supervised classification)
        np.savez_compressed(ofileNPZ, tfs=tfs)

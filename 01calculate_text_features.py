import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
import mahotas

from sentinel1denoised.S1_EW_GRD_NoiseCorrection import Sentinel1Image
from sar2ice import convert2gray, get_texture_features

# find input files
idir = '/files/sentinel1a/safefiles/'
odir = '/files/sentinel1a/odata/'
ifiles = sorted(glob.glob(idir + '*.SAFE'))

## set up parameters for Haralick texture features computation
stp = 32
ws  = 32
l   = 64
threads = 6

# if sigma0_max is None, only create histograms
#sigma0_max = None
#sigma0_min = None
sigma0_max = {'HH': -3,  'HV': -15}
sigma0_min = {'HH': -33, 'HV': -38}

r1,r2 = 0,None # no crop
c1,c2 = 0,None # no crop

# crop using the following limits (uncomment for testing only)
r1,r2 = 1000,5000
c1,c2 = 1000,5000

for ifilepath in ifiles:
    ifile = os.path.split(ifilepath)[1]
    print ifile
    for pol in ['HH', 'HV']:
        # set output file namew
        ofile = '%s_%s_' % (os.path.join(odir, ifile), pol)
        ofileHAR = ofile + 'har.npz'

        # skip processing already extisting files
        if os.path.exists(ofileHAR):
            continue

        # read data from input S1 file
        s1i = Sentinel1Image(idir + ifile)
        print 'Read sigma0_%s from %s' % (pol, ifile)
        sigma0 = s1i['sigma0_%s' % pol]
        print 'Create watermask'
        wm = s1i.watermask()[1]
        s1i = None
        del s1i

        # crop (testing only)
        sigma0 = sigma0[r1:r2, c1:c2]
        wm = wm[r1:r2, c1:c2]

        if sigma0_min is None or sigma0_max is None:
            plt.hist(sigma0[(wm != 2) * np.isfinite(sigma0)], 100)
            plt.savefig(ofile + 'sigma0_hist.jpg', dpi=100)
            plt.close()
            continue

        # make full res JPG
        plt.imsave(ofile + 'sigma0.jpg', sigma0, vmin=sigma0_min[pol], vmax=sigma0_max[pol], cmap='gray')

        # convert to integer leves
        sigma0 = convert2gray(sigma0, sigma0_min[pol], sigma0_max[pol], l)

        # mask land
        print 'mask land'
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
        np.savez_compressed(ofileHAR, tfs=tfs)

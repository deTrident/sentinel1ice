import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
import mahotas

from sentinel1denoised.S1_EW_GRD_NoiseCorrection import Sentinel1Image
from sar2ice import convert2gray, get_texture_features

# find input files
idir = '/files/sentinel1a/odata/'
odir = '/files/sentinel1a/odata/'
ifiles = sorted(glob.glob(idir + '*.SAFE_s0.npz'))

## set up parameters for Haralick texture features computation
stp = 32
ws  = 32
l   = 64
threads = 6

# if sigma0_max is None, only create histograms
#sigma0_max = None
#sigma0_min = None
sigma0_max = {'HH': -3,  'HV': -17}
sigma0_min = {'HH': -25, 'HV': -33}

for ifilepath in ifiles:
    ifile = os.path.split(ifilepath)[1]
    print ifile
    wm = None
    for pol in ['HH', 'HV']:
        # set output file namew
        ofile = '%s_%s_' % (os.path.join(odir, ifile), pol)
        ofileHAR = ofile + 'har.npz'

        # skip processing already extisting files
        if os.path.exists(ofileHAR):
            continue

        # read data from denoised NPZ
        wm = np.load(ifilepath)['wm']
        sigma0 = np.load(ifilepath)['sigma0_%s_denoised' % pol]

        # create histograms
        histfile = ofile + 'hist.png'
        if not os.path.exists(histfile):
            plt.hist(sigma0[(wm != 2) * np.isfinite(sigma0)], 100)
            plt.savefig(histfile, dpi=100)
            plt.close()

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

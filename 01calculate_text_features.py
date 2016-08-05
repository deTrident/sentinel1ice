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

        # read data from input S1 file
        s1i = Sentinel1Image(idir + ifile)
        s1i.add_denoised_band('sigma0_%s' % pol)

        # for testsing only
        s1i.crop(1000,1000, 2000, 2000)

        print 'Read sigma0_%s from %s' % (pol, ifile)
        sigma0 = s1i['sigma0_%s_denoised' % pol]

        if wm is None:
            print 'Create watermask'
            wm = s1i.watermask()[1]

        if sigma0_min is None or sigma0_max is None:
            plt.hist(sigma0[(wm != 2) * np.isfinite(sigma0)], 100)
            plt.savefig(ofile + 'sigma0_hist.jpg', dpi=100)
            plt.close()
            continue

        # make full res JPG
        s1i.write_figure(ofile + 'sigma0.jpg', 'sigma0_%s_denoised' % pol, clim=[sigma0_min[pol], sigma0_max[pol]], cmapName='gray')
        del s1i

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

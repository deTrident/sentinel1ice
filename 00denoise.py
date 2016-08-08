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

for ifilepath in ifiles:
    ifile = os.path.split(ifilepath)[1]
    results = {}
    # set output file namew
    ofile = os.path.join(odir, ifile) + '_s0.npz'
    # skip processing already extisting files
    if os.path.exists(ofile):
        continue
    for pol in ['HH', 'HV']:
        # run denoising
        print 'Run denoising of sigma0_%s in %s' % (pol, ifile)
        s1i = Sentinel1Image(idir + ifile)
        s1i.add_denoised_band('sigma0_%s' % pol)

        # for testsing only
        s1i.crop(1000,1000, 6000, 6000)

        print 'Read denoised sigma0_%s from %s' % (pol, ifile)
        results['sigma0_%s_denoised' % pol] = s1i['sigma0_%s_denoised' % pol]

        if 'wm' not in results:
            print 'Create watermask'
            results['wm'] = s1i.watermask()[1]

        # make full res JPG
        jpgfile = '%s_%s.jpg' % (ofile, pol)
        if not os.path.exists(jpgfile):
            vmin = np.percentile(results['sigma0_%s_denoised' % pol][
                                 np.isfinite(results['sigma0_%s_denoised' % pol])
                                 *(results['wm']!=2)], 1)
            vmax = np.percentile(results['sigma0_%s_denoised' % pol][
                                 np.isfinite(results['sigma0_%s_denoised' % pol])
                                 *(results['wm']!=2)], 99)
            s1i.write_figure(jpgfile, 'sigma0_%s_denoised' % pol, clim=[vmin, vmax], cmapName='gray')

        del s1i
    np.savez_compressed(ofile, **results)


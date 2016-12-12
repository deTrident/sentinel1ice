''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, zipfile, shutil
import numpy as np
from sentinel1denoised.S1_EW_GRD_NoiseCorrection import Sentinel1Image

# find input files
idir = '/Volumes/ExFAT2TB/Sentinel1A/FramStrait/'
odir = '/Volumes/ExFAT2TB/Sentinel1A/odata_FramStrait_denoised/'
ifiles = sorted(glob.glob(idir + 'S1A_EW_GRDM_1SDH*.zip'),reverse=False)

for ifile in ifiles:
    
    ifilename = os.path.split(ifile)[1]
    ofile = { 'HH': os.path.join(odir, ifilename[:-4]) + '_HH_s0.npz',
              'HV': os.path.join(odir, ifilename[:-4]) + '_HV_s0.npz' }
    if os.path.exists(ofile['HH']) and os.path.exists(ofile['HV']):
        continue
    else:
        with zipfile.ZipFile(ifile, "r") as z:
            z.extractall()
    ifilename = ifilename[:-3]+'SAFE'

    for pol in ['HH','HV']:
        
        if os.path.exists(ofile[pol]):
            continue
        results = {}
        print 'Run denoising of sigma0_%s in %s' % (pol, ifilename)
        s1i = Sentinel1Image(ifilename)
        s1i.add_band( 10*np.log10(s1i['sigma0_%s' % pol]),
                      parameters={'name':'sigma0_%s_raw' % pol} )
        ### CAUTION: gap filling should be avoided. it distorts image statistics.
        s1i.add_denoised_band( 'sigma0_%s' % pol, denoising_algorithm='NERSC',
                               reference_subswath=1, add_base_power=0,
                               fill_voids=False, dB_conversion=True )
        results['sigma0'] = s1i['sigma0_%s_denoised' % pol]
        
        # extract extra data for further denoising
        if pol == 'HV':
            results['NEsigma0'] = s1i['NEsigma0_%s' % pol]
        if 'SWbounds' not in results:
            results['SWbounds'] = s1i.get_swath_bounds(pol)

        # generate watermask
        if 'wm' not in results:
            results['wm'] = s1i.watermask()[1]

        # compute histograms
        bin_edges = np.arange(-40,+10.5,0.5)
        raw_hist = np.histogram( s1i['sigma0_%s_raw' % pol]
                                    [ np.isfinite(s1i['sigma0_%s_raw' % pol])
                                      * (results['wm']!=2) ],
                                 bins=bin_edges )
        results['raw_hist'] = raw_hist
        denoised_hist = np.histogram( results['sigma0']
                                             [ np.isfinite(results['sigma0'])
                                               * (results['wm']!=2) ],
                                      bins=bin_edges )
        results['denoised_hist'] = denoised_hist

        # create quickview
        print 'Make full resolution JPG'
        jpgfile = ofile[pol][:-4] + '.jpg'
        vmin = np.percentile( results['sigma0'][ np.isfinite(results['sigma0'])
                                                 * (results['wm']!=2) ], 1. )
        vmax = np.percentile( results['sigma0'][ np.isfinite(results['sigma0'])
                                                 * (results['wm']!=2) ], 99. )
        s1i.write_figure( jpgfile, 'sigma0_%s_denoised' % pol,
                          clim=[vmin, vmax], cmapName='gray')
        #s1i.write_figure( jpgfile[:-4]+'.jpeg', 'sigma0_%s_raw' % pol,
        #                  clim=[vmin, vmax], cmapName='gray' )

        # save denoised data
        np.savez_compressed(ofile[pol] , **results)
        del s1i

    if os.path.exists(ifilename):
        shutil.rmtree(ifilename)

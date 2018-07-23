### DENOISE HH/HV IMAGES AND SAVE THEM WITH SOME OF THEIR CORRESPONDNIG ATTRIBUTES.
### USE THIS IF THE COMPUTATIONAL RESOURCES ARE ENOUGH TO RUN PARALLEL PROCESSING.

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, zipfile, shutil
import numpy as np
from scipy.ndimage import maximum_filter
from multiprocessing import Pool
from sentinel1denoised.S1_TOPS_GRD_NoiseCorrection import Sentinel1Image
from sar2ice import convert2gray
from config import get_env

# read configuration
env = get_env()
minDate = env['minDate']
maxDate = env['maxDate']
idir = env['inputDirectory']
wildcard = env['wildcard']
ws  = env['subwindowSize']    # 1km pixel spacing (40m * 25 = 1000m)
stp = get_env()['stepSize']
gamma0_max = env['gamma0_max']
gamma0_min = env['gamma0_min']
l   = env['grayLevel']    # gray-level.

# define process
def run_process(ifile):
    ifilename = os.path.split(ifile)[1]
    ID = ifilename.split('.')[0]
    wdir = os.path.join(env['outputDirectory'], ID)
    if not os.path.exists(wdir):
        os.mkdir(wdir)
    ofile = os.path.join(wdir,ID+'_gamma0.npz')
    if os.path.exists(ofile):
        print('Processed data file already exists.')
    if env['unzipInput']:
        with zipfile.ZipFile(ifile, "r") as z:
            z.extractall()
        ifilename = ifilename[:-3]+'SAFE'
    else:
        ifilename = ifile
    results = {}
    s1i = Sentinel1Image(ifilename)
    # denoise dual-pol images
    for pol in ['HH','HV']:
        print('Denoising for %s polarization image in %s' % (pol, ifilename))
        s1i.add_band(array=s1i.rawSigma0Map(polarization=pol),
                     parameters={'name':'sigma0_%s_original' % pol})
        s1i.add_band(array=(s1i.thermalNoiseRemoval_dev(polarization=pol, windowSize=ws)
                            / np.cos(np.deg2rad(s1i['incidence_angle']))),
                     parameters={'name':'gamma0_%s_denoised' % pol})
    # landmask generation.
    s1i.add_band(array=maximum_filter(s1i.landmask(skipGCP=4).astype(uint8), ws),
                 parameters={'name':'landmask'})
    # compute histograms and apply gray level scaling
    bin_edges = np.arange(-40.0,+10.1,0.1)
    for pol in ['HH','HV']:
        valid = (s1i['landmask']!=1)
        sigma0dB = 10*np.log10(s1i['sigma0_%s_original' % pol])
        results['original_sigma0_%s_hist' % pol] = np.histogram(
            sigma0dB[np.isfinite(sigma0dB) * valid], bins=bin_edges )
        gamma0dB = 10*np.log10(s1i['gamma0_%s_denoised' % pol])
        results['denoised_gamma0_%s_hist' % pol] = np.histogram(
            gamma0dB[np.isfinite(gamma0dB) * valid], bins=bin_edges )
        results['gamma0_%s' % pol] = convert2gray(gamma0dB, gamma0_min[pol], gamma0_max[pol], l)
        results['gamma0_%s' % pol][np.logical_not(valid)] = 0
    # quickview
    s1i.resize(factor=1./stp)
    for pol in ['HH','HV']:
        valid = (s1i['landmask']!=1)
        s1i.export(ofile.replace('_gamma0.npz','_original_sigma0_%s.tif' % pol),
                   bands=[s1i.get_band_number('sigma0_%s_original' % pol)], driver='GTiff')
        s1i.export(ofile.replace('_gamma0.npz','_denoised_gamma0_%s.tif' % pol),
                   bands=[s1i.get_band_number('gamma0_%s_denoised' % pol)], driver='GTiff')
        sigma0dB = 10*np.log10(s1i['sigma0_%s_original' % pol])
        vmin, vmax = np.percentile(sigma0dB[np.isfinite(sigma0dB) * valid], (1,99))
        plt.imsave( ofile.replace('_gamma0.npz','_original_sigma0_%s.png' % pol),
                    sigma0dB, vmin=vmin, vmax=vmax, cmap='gray' )
        gamma0dB = 10*np.log10(s1i['gamma0_%s_denoised' % pol])
        vmin, vmax = np.percentile(gamma0dB[np.isfinite(gamma0dB) * valid], (1,99))
        plt.imsave( ofile.replace('_gamma0.npz','_denoised_gamma0_%s.png' % pol),
                    gamma0dB, vmin=vmin, vmax=vmax, cmap='gray' )
    # incidence angle
    results['incidenceAngle'] = s1i['incidence_angle']
    # save the results as a npz file
    np.savez_compressed(ofile, **results)
    # clean up
    del s1i
    if os.path.exists(ifilename) and env['unzipInput']:
        shutil.rmtree(ifilename)

# listup S-1 SAFE files and filter by dates
ifiles = sorted(glob.glob(idir + wildcard),reverse=True)
if (minDate!=None) and (maxDate!=None):
    ifiles = [ifile for ifile in ifiles
        if minDate <= os.path.split(ifile)[-1][17:25] <= maxDate ]
# run parallel processing
pool = Pool(env['numberOfThreads'])
pool.map(run_process, ifiles)

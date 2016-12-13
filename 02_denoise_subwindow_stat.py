''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sar2ice import convert2gray
from sentinel1corrected.correction_model import S1_EW_GRD_StatCorrection
from PIL import Image

# find input files
idir = '/Volumes/ExFAT2TB/Sentinel1A/odata_FramStrait_denoised/'
odir = '/Volumes/ExFAT2TB/Sentinel1A/odata_FramStrait_corrected/'
ifiles = sorted(glob.glob(idir + 'S1A_EW_GRDM_1SDH*_s0.npz'),reverse=False)

# set up parameters for Haralick texture features computation later
# stp and ws must be same to them in '03_calculate_text_features.py'
ws  = 25    # 1km pixel spacing (40m * 25 = 1000m)

for ifile in ifiles:
    
    ifilename = os.path.split(ifile)[1]
    pol = ifilename[68:70]
    ofile = os.path.join(odir, ifilename)
    if os.path.exists(ofile):
        continue

    # run denoising and save results.
    print('Run denoising of sigma0 in: %s' % ifilename)
    S1_EW_GRD_StatCorrection(ifile,ofile,pol,ws)

    # create quickview
    print 'Make full resolution JPG'
    jpgfile = ofile[:-4] + '.jpg'
    sigma0 = np.load(ofile)['sigma0']
    wm = np.load(ofile)['wm']
    vmin, vmax = np.percentile( sigma0[np.isfinite(sigma0)*(wm!=2)], (1.,99.) )
    Image.fromarray(convert2gray(sigma0,vmin,vmax,255)).convert('RGB').save(jpgfile)

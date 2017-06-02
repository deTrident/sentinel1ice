''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sentinel1denoised.S1_EW_GRD_NoiseCorrection import Sentinel1Image
from sar2ice import get_map, export_uint8_jpeg, export_uint8_png, export_PS_proj_GTiff
from config import get_env

env = get_env()

# find input files
idir = env['inputDirectory']
odir = env['outputDirectory']
ifiles = sorted(glob.glob(env['inputDirectory'] + env['wildcard']))


for ifile in ifiles:
    
    ID = os.path.split(ifile)[1].split('.')[0]
    if not os.path.exists(odir+ID):
        os.mkdir(odir+ID)
    if os.path.exists(os.path.join(odir+ID,ID+'_svm_zones.png')):
        continue
    print ID
    s1i = Sentinel1Image(ifile)
    sigma0, tfs, pca_zones, svm_zones = get_map(s1i,env)

    export_uint8_jpeg( os.path.join(odir+ID,ID+'_HH_sigma0.jpg'), sigma0['HH'] )
    export_uint8_jpeg( os.path.join(odir+ID,ID+'_HV_sigma0.jpg'), sigma0['HV'] )
    export_uint8_png(os.path.join(odir+ID,ID+'_pca_zones.png'), pca_zones)
    export_PS_proj_GTiff(pca_zones,ifile,os.path.join(odir+ID,ID+'_geocoded_pca_zones.tif'))
    export_uint8_png(os.path.join(odir+ID,ID+'_svm_zones.png'), svm_zones)
    export_PS_proj_GTiff(svm_zones,ifile,os.path.join(odir+ID,ID+'_geocoded_svm_zones.tif'))

    for i in range(13):
        export_uint8_png( os.path.join(odir+ID,ID+'_HH_har%02d_norm.jpg' % i), tfs[i] )
        export_uint8_png( os.path.join(odir+ID,ID+'_HV_har%02d_norm.jpg' % i), tfs[i+13] )

    del s1i, sigma0, tfs, pca_zones, svm_zones

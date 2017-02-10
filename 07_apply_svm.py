''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sentinel1denoised.S1_EW_GRD_NoiseCorrection import Sentinel1Image
from sar2ice import get_map
from config import get_env


# find input files
idir = get_env()['inputDirectory']
odir = get_env()['outputDirectory']
ifiles = sorted(glob.glob(idir + 'S1A_EW_GRDM_1SDH*.zip'),reverse=False)

mLook = get_env()['multiLookFactor']
vmax = get_env()['sigma0_max']
vmin = get_env()['sigma0_min']
stp = get_env()['stepSize']    # step size
ws  = get_env()['subwindowSize']    # 1km pixel spacing (40m * 25 = 1000m)
l   = get_env()['grayLevel']    # gray-level. 32 or 64.
threads = get_env()['numberOfThreads']
tfAlg = get_env()['textureFeatureAlgorithm']
normFiles = { 'HH':get_env()['textureFeatureNormalizationFilePrefix']+'HH.npz',
              'HV':get_env()['textureFeatureNormalizationFilePrefix']+'HV.npz' }
svmFile = get_env()['supportVectorMachineFile']

for ifile in ifiles:
    
    ID = os.path.split(ifile)[1].split('.')[0]
    if not os.path.exists(odir+ID):
        os.mkdir(odir+ID)
    if os.path.exists(os.path.join(odir+ID,ID+'_svm_zones.png')):
        continue
    print ID
    s1i = Sentinel1Image(ifile)
    sigma0, iceMask = get_map(
        s1i, mLook, vmin, vmax,l, ws, stp, tfAlg, threads, normFiles, svmFile )
    plt.imsave( os.path.join(odir+ID,ID+'_HH_sigma0.jpg'),
                sigma0['HH'], cmap='gray' )
    plt.imsave( os.path.join(odir+ID,ID+'_HV_sigma0.jpg'),
                sigma0['HV'], cmap='gray' )
    plt.imsave(os.path.join(odir+ID,ID+'_svm_zones.png'), iceMask)

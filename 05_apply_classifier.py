### APPLY CLASSIFIER TO THE PRE-COMPUTED TEXTURE FEATURES

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, pickle
import numpy as np
from nansat import Nansat
from sar2ice import colorDict
from config import get_env

# read configuration
env = get_env()
classifierFilename = env['classifierFilename']
sourceType = env['sourceType']
threads = env['numberOfThreads']
# import classifier
plk = pickle.load(open(classifierFilename, "rb" ))
if type(plk)==list:
    scaler, clf = plk
else:
    class dummy_class(object):
        def transform(self, x):
            return(x)
    scaler = dummy_class()
    clf = plk
clf.n_jobs = threads
# listup texture feature files
idir = get_env()['outputDirectory']
ifiles = sorted(glob.glob(idir + '*/S1?_EW_GRDM_1SDH*_texture_features.npz'))
# process each file
for ifile in ifiles:
    ofile = ifile.replace('_texture_features.npz', '_classified.tif')
    print(ifile)
    if os.path.exists(ofile):
        print('Processed data file already exists.')
        continue
    npz = np.load(ifile)
    features = np.vstack([npz['textureFeatures'].item()['HH'],
                          npz['textureFeatures'].item()['HV'],
                          npz['incidenceAngle'][np.newaxis,:,:]])
    imgSize = features.shape[1:]
    features = features.reshape((27,np.prod(imgSize))).T
    gpi = np.isfinite(features.sum(axis=1))
    result = clf.predict(scaler.transform(features[gpi,:]))
    classImage = np.ones(np.prod(imgSize)) * np.nan
    classImage[gpi] = result
    classImage = classImage.reshape(imgSize)
    nansatObjGamma0 = Nansat(ifile.replace('_texture_features.npz','_denoised_gamma0_HH.tif'))
    if nansatObjGamma0.shape() != imgSize:
        nansatObjGamma0.crop(0,0,imgSize[1],imgSize[0])
    nansatObjClass = Nansat(array=classImage, domain=nansatObjGamma0)
    nansatObjClass.export(ofile, bands=[1], driver='GTiff')
    rgb = np.zeros((imgSize[0], imgSize[1], 3), 'uint8')
    for k in colorDict[sourceType].keys():
        rgb[classImage==k,:] = colorDict[sourceType][k]
    plt.imsave(ofile.replace('.tif','.png'), rgb)

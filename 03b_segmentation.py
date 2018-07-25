### MAKE SEGMENTATION IMAGE IN ORDER TO HELP MANUAL CLASSIFICATION

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, pickle
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from nansat import Nansat
from config import get_env

# set up parameters for clustering
n_components = 7
n_clusters = 8
# read configuration
env = get_env()
idir = env['outputDirectory']
threads = env['numberOfThreads']
kmeansFilename = env['kmeansFilename']
# listup texture feature files
ifiles = sorted(glob.glob(idir + '*/*_texture_features.npz'))
#ifiles = [fn for fn in ifiles
#          if os.path.exists(fn.replace('_texture_features.npz','_reprojected_ice_chart.tif'))]
# import and stack
features_all = []
print('*** Importing files from:')
for li, ifile in enumerate(ifiles):
    print('[%d/%d] %s' % (li+1, len(ifiles), ifile))
    npz = np.load(ifile)
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    incAng = npz['incidenceAngle'][np.newaxis,:,:]
    features_all.append(np.vstack([tfsHH,tfsHV,incAng]).reshape(27,np.prod(incAng.shape)))
features_all = np.hstack(features_all).T
features_all = features_all[np.isfinite(features_all.sum(axis=1))]
# fit PCA and KMeans
print('*** Optimizing PCA and Kmeans')
scaler = preprocessing.QuantileTransformer(output_distribution='normal').fit(features_all)
pca = PCA(n_components=n_components).fit(scaler.transform(features_all))
kmeans = KMeans(n_clusters=n_clusters, n_jobs=threads).fit(pca.transform(scaler.transform(features_all)))
pickle.dump([scaler, pca, kmeans], open(kmeansFilename, "wb" ))
# apply clustering
print('*** Exporting files to:')
for li, ifile in enumerate(ifiles):
    ofile = ifile.replace('_texture_features.npz', '_kmeans_clustered.tif')
    print('[%d/%d] %s' % (li+1, len(ifiles), ifile.replace('_texture_features.npz','_kmeans.tif')))
    npz = np.load(ifile)
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    incAng = npz['incidenceAngle'][np.newaxis,:,:]
    imgSize = tfsHH.shape[1:]
    features = np.vstack([tfsHH,tfsHV,incAng]).reshape(27,np.prod(imgSize)).T
    gpi = np.isfinite(features.sum(axis=1))
    kmeansZones = np.ones(np.prod(imgSize)) * np.nan
    kmeansZones[gpi] = kmeans.predict(pca.transform(scaler.transform(features[gpi])))
    kmeansZones = kmeansZones.reshape(imgSize)
    nansatObjGamma0 = Nansat(ifile.replace('_texture_features.npz','_denoised_gamma0_HH.tif'))
    if nansatObjGamma0.shape() != imgSize:
        nansatObjGamma0.crop(0,0,imgSize[1],imgSize[0])
    nansatObjCluster = Nansat(array=kmeansZones, domain=nansatObjGamma0)
    nansatObjCluster.export(ofile, bands=[1], driver='GTiff')
    plt.imsave(ofile.replace('.tif','.png'), kmeansZones)

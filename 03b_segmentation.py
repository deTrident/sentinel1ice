### MAKE SEGMENTATION IMAGE IN ORDER TO HELP MANUAL CLASSIFICATION

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, pickle
import numpy as np
from sklearn.preprocessing import QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from nansat import Nansat
import config as cfg


# listup texture feature files
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/*_texture_features.npz'))
if (cfg.minDate!=None) and (cfg.maxDate!=None):
    ifiles = [f for f in ifiles if cfg.minDate <= os.path.split(f)[-1][17:25] <= cfg.maxDate]
# import and stack
features_all = []
print('*** Importing files from:')
for li, ifile in enumerate(ifiles):
    print('[%d/%d] %s' % (li+1, len(ifiles), ifile))
    npz = np.load(ifile)
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    features_all.append(np.vstack([tfsHH,tfsHV]).reshape(26,np.prod(tfsHH.shape[1:])))
features_all = np.hstack(features_all).T
features_all = features_all[np.isfinite(features_all.sum(axis=1))]
# fit PCA and KMeans
print('*** Optimizing PCA and Kmeans')
scaler = QuantileTransformer(output_distribution='normal').fit(features_all)
pca = PCA(n_components=26).fit(scaler.transform(features_all))
n_components = len(np.where(np.cumsum(pca.explained_variance_ratio_) < cfg.pcaVarThres)[0])+1
kmeans = KMeans(n_clusters=9, n_jobs=cfg.numberOfThreads).fit(
             pca.transform(scaler.transform(features_all))[:,:n_components])
pickle.dump([scaler, pca, n_components, kmeans], open(cfg.kmeansFilename, "wb" ))
# apply clustering
print('*** Exporting files to:')
for li, ifile in enumerate(ifiles):
    ofile = ifile.replace('_texture_features.npz', '_kmeans_clustered.tif')
    print('[%d/%d] %s' % (li+1, len(ifiles), ifile.replace('_texture_features.npz','_kmeans.tif')))
    npz = np.load(ifile)
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    imgSize = tfsHH.shape[1:]
    features = np.vstack([tfsHH,tfsHV]).reshape(26,np.prod(imgSize)).T
    gpi = np.isfinite(features.sum(axis=1))
    kmeansZones = np.zeros(np.prod(imgSize))    # 0 is reserved for void cells
    kmeansZones[gpi] = 1 + kmeans.predict(
                               pca.transform(scaler.transform(features[gpi]))[:,:n_components])
    kmeansZones = kmeansZones.reshape(imgSize)
    nansatObjSigma0 = Nansat(ifile.replace('_texture_features.npz','_sigma0_HH_denoised.tif'))
    if nansatObjSigma0.shape() != imgSize:
        nansatObjSigma0.crop(0,0,imgSize[1],imgSize[0])
    nansatObjCluster = Nansat.from_domain(array=kmeansZones.astype(np.uint8), domain=nansatObjSigma0)
    nansatObjCluster.export(ofile, bands=[1], driver='GTiff')
    if cfg.quicklook:
        plt.imsave(ofile.replace('.tif','.png'), kmeansZones, cmap='tab10')

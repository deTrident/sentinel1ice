import os
import glob

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import zoom

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

idir = '/files/sentinel1a/odata/'
n_components=6
n_clusters=15

ifiles = sorted(glob.glob(idir + '*_HH_har_norm.npz'))

# load all normalized TFs from input files
joinedTF = []
for ifile in ifiles:
    print ifile
    hhhvTF = []
    for pol in ['HH', 'HV']:
        # load normalized TF from HH or HV as 3D cubes (13 x rows x cols)
        ifilename = ifile.replace('HH', pol)
        harData = np.load(ifilename)['tfsNorm']
        # join TFs into single 2D matrix (26 x rows*cols)
        hhhvTF.append(harData.reshape(13, harData.shape[1]*harData.shape[2]))
    joinedTF.append(np.vstack(hhhvTF))
# stack together TFs from all input images
joinedTF = np.hstack(joinedTF)

ofile = idir + 'joined_'

# select good pixels only
gpi = np.isfinite(joinedTF.sum(axis=0))

# run PCA to reduce dimensionality and keep information
print 'run PCA'
pcaDataGood = PCA(n_components=n_components).fit_transform(joinedTF[:, gpi].T)

# run automatic unsupervised classification using k-means
print 'run KMeans'
lablesGood = KMeans(n_clusters=n_clusters).fit_predict(pcaDataGood[:, :n_components])

# make scatter plots with (1st vs 2nd and 3rd vs 4th) principal components
# colored by clusters
print 'make scatter plots'
plt.scatter(pcaDataGood[:, 0], pcaDataGood[:, 1], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter01.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.close('all')

plt.scatter(pcaDataGood[:, 1], pcaDataGood[:, 2], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter12.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.close('all')

# paste good PC and labels data into full size matrix
pcaDataAll = np.zeros((n_components, joinedTF.shape[1])) + np.nan
pcaDataAll[:, gpi] = pcaDataGood.T

labelsAll = np.zeros(joinedTF.shape[1]) + np.nan
labelsAll[gpi] = lablesGood

#%cpaste
# save PCs and labels in input-specific files
pointer = 0
for ifilepath in ifiles:
    print 'save PCA to', ifilepath
    # load sample data just to get the shape of the inut grid
    harData = np.load(ifilepath)['tfsNorm']
    harDataSize = harData.shape[1]*harData.shape[2]
    # fetch PCA and lables for that image values from matrix with all data
    pcaData = pcaDataAll[:, pointer:pointer+harDataSize].reshape(n_components, harData.shape[1], harData.shape[2])
    labels = labelsAll[pointer:pointer+harDataSize].reshape(harData.shape[1], harData.shape[2])
    pointer += harDataSize

    # save PCA and labels data
    ofile = ifilepath.replace('HH_har_norm', 'pca_zones')
    np.savez_compressed(ofile, pcaData=pcaData, labels=labels)

    # vis. spatial distribution of PCAs and labels (map of zones)
    for ipc, pc in enumerate(pcaData):
        plt.imsave(ifilepath.replace('HH_har_norm', 'pc%02d' % ipc) + '.png', pc)

    # save full-size zones (zoom WS-times)
    labels_ms = np.zeros((labels.shape[0] + 1, labels.shape[1] + 1)) + np.nan
    labels_ms[:labels.shape[0], :labels.shape[1]] = labels
    sigma0fs = plt.imread(ifilepath.replace('_har_norm.npz', '.jpg'))
    labels_fs = zoom(labels_ms, sigma0fs.shape[0] / labels_ms.shape[0], order=0)
    plt.imsave(ifilepath.replace('HH_har_norm', 'zones') + '.png', labels_fs)


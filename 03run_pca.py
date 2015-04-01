import os
import glob

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

idir = '/files/sentinel1a/odata/'
n_components=6

ifiles = sorted(glob.glob(idir + '*_HH_har_norm.npz'))

# load all normalized TFs from input files
joinedTF = []
for ifile in ifiles:
    print ifile
    hhhvTF = []
    for pol in ['HH', 'HV']:
        ifilename = ifile.replace('HH', pol)
        harData = np.load(ifilename)['newTFData%s' % pol]
        hhhvTF.append(harData.reshape(13, harData.shape[1]*harData.shape[2]))
    joinedTF.append(np.vstack(hhhvTF))
joinedTF = np.hstack(joinedTF)

ofile = idir + 'all_files_'

# select good pixels only
gpi = np.isfinite(joinedTF.sum(axis=0))

# run PCA
print 'run PCA'
pcaDataGood = PCA(n_components=n_components).fit_transform(joinedTF[:, gpi].T)

# run k-means
print 'run KMeans'
lablesGood = KMeans(n_clusters=15).fit_predict(pcaDataGood[:, :3])

# make scatter plots
print 'make scatter plots'
plt.scatter(pcaDataGood[:, 0], pcaDataGood[:, 1], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter01.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.close('all')

plt.scatter(pcaDataGood[:, 1], pcaDataGood[:, 2], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter12.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.close('all')

# save PCs and Zones in input-specific files
pcaDataAll = np.zeros((n_components, joinedTF.shape[1])) + np.nan
pcaDataAll[:, gpi] = pcaDataGood.T

labelsAll = np.zeros(joinedTF.shape[1]) + np.nan
labelsAll[gpi] = lablesGood

#%cpaste
pointer = 0
for ifilepath in ifiles:
    print 'save PCA to', ifilepath
    harData = np.load(ifilepath)['newTFDataHH']
    harDataSize = harData.shape[1]*harData.shape[2]
    pcaData = pcaDataAll[:, pointer:pointer+harDataSize].reshape(n_components, harData.shape[1], harData.shape[2])
    labels = labelsAll[pointer:pointer+harDataSize].reshape(harData.shape[1], harData.shape[2])
    pointer += harDataSize

    ofile = ifilepath.replace('HH_har_norm', 'pca_zones')
    np.savez_compressed(ofile, pcaData=pcaData, labels=labels)
    for ipc, pc in enumerate(pcaData):
        plt.imsave(ifilepath.replace('HH_har_norm', 'pc%02d' % ipc) + '.png', pc)
    plt.imsave(ifilepath.replace('HH_har_norm', 'zones') + '.png', labels)


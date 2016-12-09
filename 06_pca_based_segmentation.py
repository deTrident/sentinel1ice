''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from scipy.ndimage.interpolation import zoom
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

idir = ( os.path.abspath(os.getcwd()+'/../shared/test_data/sentinel1a_l1')
         +'/odata_FramStrait_TFs/' )
n_components = 6
n_clusters = 15
tfsID = range(13)

ifiles = sorted(glob.glob(idir + '*_HH_har_norm.npz'))

# load all normalized TFs from input files
joinedTF = []
for ifile in ifiles:
    print ifile
    hhhvTF = []
    for pol in ['HH', 'HV']:
        # load normalized TF from HH or HV as 3D cubes (13 x rows x cols)
        harData = np.load(ifile.replace('_HH_', '_%s_' % pol))['tfsNorm'][tfsID,:,:]
        # join TFs into single 2D matrix (26 x rows*cols)
        hhhvTF.append(harData.reshape(len(tfsID), harData.shape[1]*harData.shape[2]))
    joinedTF.append(np.vstack(hhhvTF))
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

# make scatter plots with (1st vs 2nd and 2nd vs 3rd) principal components
# colored by clusters
print 'make scatter plots'
plt.scatter(pcaDataGood[:, 0], pcaDataGood[:, 1], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter01.png', dpi=150, bbox_inches='tight', pad_inches=0)
plt.close('all')
plt.scatter(pcaDataGood[:, 1], pcaDataGood[:, 2], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter12.png', dpi=150, bbox_inches='tight', pad_inches=0)
plt.close('all')
plt.scatter(pcaDataGood[:, 2], pcaDataGood[:, 3], 1, lablesGood, linewidths=0)
plt.savefig(ofile + 'scatter23.png', dpi=150, bbox_inches='tight', pad_inches=0)
plt.close('all')

# paste good PC and labels data into full size matrix
pcaDataAll = np.zeros((n_components, joinedTF.shape[1])) + np.nan
pcaDataAll[:, gpi] = pcaDataGood.T
labelsAll = np.zeros(joinedTF.shape[1]) + np.nan
labelsAll[gpi] = lablesGood

# save PCs and labels in input-specific files
pointer = 0
for ifile in ifiles:
    print 'save PCA to', os.path.split(ifile)[1]
    # load sample data just to get the shape of the input grid
    harDataShape = np.load(ifile)['tfsNorm'][tfsID,:,:].shape
    harDataSize = harDataShape[1]*harDataShape[2]
    # fetch PCA and lables for that image values from matrix with all data
    pcaData = pcaDataAll[:, pointer:pointer+harDataSize].reshape(
                  n_components, harDataShape[1], harDataShape[2] )
    labels = labelsAll[pointer:pointer+harDataSize].reshape(
                 harDataShape[1], harDataShape[2] )
    pointer += harDataSize

    # save PCA and labels data
    ofile = ifile.replace('HH_har_norm', 'pca_zones')
    np.savez_compressed(ofile, pcaData=pcaData, labels=labels)

    # vis. spatial distribution of PCAs and labels (map of zones)
    for ipc, pc in enumerate(pcaData):
        plt.imsave(ifile.replace('HH_har_norm', 'pc%02d' % ipc) + '.png', pc)

    # save full-size zones (zoom WS-times)
    labels_ms = np.zeros((labels.shape[0]+1, labels.shape[1]+1)) + np.nan
    labels_ms[:labels.shape[0], :labels.shape[1]] = labels
    fs_dim = np.load(ifile)['proc_params'].item()['input_dimension']
    labels_fs = zoom(labels_ms, fs_dim[0] / labels_ms.shape[0], order=0)
    plt.imsave(ifile.replace('HH_har_norm', 'zones') + '.png', labels_fs)

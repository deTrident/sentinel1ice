### TRAIN SUPPORT VECTOR MACHINE BASED CLASSIFIER

import os, glob, pickle, gdal
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import QuantileTransformer
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.ensemble import BaggingClassifier
import config as cfg


samplesPerEnsembleClassifier = int((10000/cfg.stepSize)**2)

# read configuration
if cfg.sourceType=='manual':
    ext = '_manual_classification.tif'
else:
    ext = '_reprojected_%s.tif' % cfg.sourceType

# listup reprojected ice charts
ifiles = sorted(glob.glob(cfg.outputDirectory+'*/*%s' % ext))
ifiles = [f for f in ifiles if os.path.exists(f.replace(ext, '_texture_features.npz'))]
if (cfg.minDate!=None) and (cfg.maxDate!=None):
    ifiles = [f for f in ifiles
              if cfg.minDate <= os.path.split(f)[-1][17:25] <= cfg.maxDate]

# import and stack
features_all = []
iceCodes_all = []
print('*** Importing files from:')
for li, ifile in enumerate(ifiles):
    print('[%d/%d] %s' % (li+1, len(ifiles), os.path.dirname(ifile)))
    npz = np.load(ifile.replace(ext, '_texture_features.npz'))
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    iceCode = gdal.Open(ifile).ReadAsArray()
    features_all.append(np.vstack([tfsHH,tfsHV]).reshape(26,np.prod(iceCode.shape)))
    iceCodes_all.append(iceCode.reshape(np.prod(iceCode.shape)))
features_all = np.hstack(features_all).T
iceCodes_all = np.hstack(iceCodes_all).T

# exclude some ice codes (98:glacier, 99:undefined, 107:fast ice, 108:iceberg, 255:land)
gpi = ( np.isfinite(features_all.sum(axis=1)) * (iceCodes_all != 98) * (iceCodes_all != 99)
        * (iceCodes_all != 107) * (iceCodes_all != 108) * (iceCodes_all != 255) )
features_all = features_all[gpi]
iceCodes_all = iceCodes_all[gpi]

### data reduction
print('*** Dimensionality reduction using PCA.')
scaler = QuantileTransformer(output_distribution='normal').fit(features_all)
pca = PCA(n_components=26).fit(scaler.transform(features_all))
n_components = len(np.where(np.cumsum(pca.explained_variance_ratio_) < cfg.pcaVarThres)[0])+1

### divide data into train/test set
test_size = (1. - cfg.maxNumberOfSamplesToTrain/len(iceCodes_all))
if test_size <= 0:
    test_size = 0.3
trainFeatures, testFeatures, trainZones, testZones = train_test_split(
    features_all, iceCodes_all, test_size=test_size)

### tune hyper-parameters
print('*** Tuning hyper-parameters.')
tuneFeatures = pca.transform(scaler.transform(
    trainFeatures[:np.min([samplesPerEnsembleClassifier, len(trainFeatures)])]))[:,:n_components]
tuneZones = trainZones[:np.min([samplesPerEnsembleClassifier, len(trainFeatures)])]
grid_lin = GridSearchCV(svm.LinearSVC(),
                        param_grid={'C':np.logspace(-1,1,3,base=10).tolist()},
                        n_jobs=cfg.numberOfThreads, verbose=10)
grid_lin.fit(tuneFeatures, tuneZones)
grid_rbf = GridSearchCV(svm.SVC(kernel='rbf'),
                        param_grid={'gamma':np.logspace(-1,1,3,base=10).tolist(),
                                    'C':np.logspace(-1,1,3,base=10).tolist()},
                        n_jobs=cfg.numberOfThreads, verbose=10)
grid_rbf.fit(tuneFeatures, tuneZones)
if grid_lin.best_score_ >= grid_rbf.best_score_:
    estimator = svm.LinearSVC(**grid_lin.best_params_)
else:
    physical_memory_in_MB = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024.**2)
    cache_size = np.median([200, 1024, physical_memory_in_MB // cfg.numberOfThreads])
    estimator = svm.SVC(kernel='rbf', **grid_rbf.best_params_, cache_size=cache_size)

### train classifier
print('*** Training classifier: %d samples.' % len(trainZones))
n_estimators = np.max([1, len(trainZones) // samplesPerEnsembleClassifier])
max_samples = 1./n_estimators
clf = BaggingClassifier(base_estimator=estimator, n_jobs=cfg.numberOfThreads, verbose=10,
                        n_estimators=n_estimators, max_samples=max_samples)
clf.fit(pca.transform(scaler.transform(trainFeatures))[:,:n_components], trainZones)
pickle.dump([scaler, pca, n_components, clf], open(cfg.classifierFilename, "wb" ))

### test classifier
scaler, pca, n_components, clf = pickle.load(open(cfg.classifierFilename, "rb" ))
print('*** Testing classifier: %d samples.' % len(testZones))
result = clf.predict(pca.transform(scaler.transform(testFeatures))[:,:n_components])
print('classID    nSamples    accuracy')
for uniqueValue in np.unique(testZones):
    testPixel = (testZones == uniqueValue)
    badPixel = (result[testPixel] != uniqueValue)
    print('%7s    %8d     %6.3f%%'
          % (uniqueValue, len(testPixel[testPixel]),
             (1 - badPixel[badPixel].sum() / float(testPixel[testPixel].sum()))*100 ))

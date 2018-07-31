### TRAIN SUPPORT VECTOR MACHINE BASED CLASSIFIER

import os, glob, pickle, gdal
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn import svm, preprocessing
from sklearn.ensemble import BaggingClassifier
import config as cfg

# read configuration
if cfg.sourceType=='manual':
    ext = '_manual_classification.tif'
else:
    ext = '_reprojected_%s.tif' % cfg.sourceType
# set up parameters for training
trainProportion = 0.6
samplesPerEnsembleClassifier = int((10000/cfg.stepSize)**2)
# listup reprojected ice charts
ifiles = sorted(glob.glob(cfg.outputDirectory+'*/*%s' % ext))
# import and stack
features_all = []
iceCodes_all = []
print('*** Importing files from:')
for li, ifile in enumerate(ifiles):
    print('[%d/%d] %s' % (li+1, len(ifiles), os.path.dirname(ifile)))
    npz = np.load(ifile.replace(ext, '_texture_features.npz'))
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    incAng = npz['incidenceAngle'][np.newaxis,:,:]
    iceCode = gdal.Open(ifile).ReadAsArray()
    features_all.append(np.vstack([tfsHH,tfsHV,incAng]).reshape(27,np.prod(iceCode.shape)))
    iceCodes_all.append(iceCode.reshape(np.prod(iceCode.shape)))
features_all = np.hstack(features_all).T
iceCodes_all = np.hstack(iceCodes_all).T
# exclude some ice codes (98:glacier, 99:undefined, 107:fast ice, 108:iceberg)
gpi = ( np.isfinite(features_all.sum(axis=1)) * (iceCodes_all != 98) * (iceCodes_all != 99)
        * (iceCodes_all != 107) * (iceCodes_all != 108) )
features_all = features_all[gpi]
iceCodes_all = iceCodes_all[gpi]
### divide data into train/test set
trainIndices = []
testIndices = []
for uv in np.unique(iceCodes_all):
    uvIndices = np.where(iceCodes_all==uv)[0]
    sampleIndices = uvIndices[np.random.permutation(len(uvIndices))]
    nTrain = int(len(uvIndices) * trainProportion)
    trainIndices.append(sampleIndices[:nTrain])
    testIndices.append(sampleIndices[nTrain:])
trainIndices = np.hstack(trainIndices)
trainIndices = trainIndices[np.random.permutation(len(trainIndices))]
testIndices = np.hstack(testIndices)
testIndices = testIndices[np.random.permutation(len(testIndices))]
### tune hyper-parameters
print('*** Tuning hyper-parameters.')
tuneIndices = trainIndices[:np.min([samplesPerEnsembleClassifier, len(trainIndices)])]
tuneScaler = preprocessing.QuantileTransformer(output_distribution='normal').fit(features_all[tuneIndices])
tuneFeatures = tuneScaler.transform(features_all[tuneIndices])
tuneZones = iceCodes_all[tuneIndices]
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
print('*** Training classifier: %d samples.' % len(trainIndices))
scaler = preprocessing.QuantileTransformer(output_distribution='normal').fit(features_all[trainIndices])
trainFeatures = scaler.transform(features_all[trainIndices,:])
trainZones = iceCodes_all[trainIndices]
n_estimators = np.max([1, len(trainIndices) // samplesPerEnsembleClassifier])
max_samples = 1./n_estimators
clf = BaggingClassifier(base_estimator=estimator, n_jobs=cfg.numberOfThreads, verbose=10,
                        n_estimators=n_estimators, max_samples=max_samples)
clf.fit(trainFeatures, trainZones)
pickle.dump([scaler, clf], open(cfg.classifierFilename, "wb" ))
### test classifier
print('*** Testing classifier: %d samples.' % len(testIndices))
testFeatures = scaler.transform(features_all[testIndices,:])
testZones = iceCodes_all[testIndices]
result = clf.predict(testFeatures)
print('classID    nSamples    accuracy')
for uniqueValue in np.unique(testZones):
    testPixel = (testZones == uniqueValue)
    badPixel = (result[testPixel] != uniqueValue)
    print('%7s    %8d     %6.3f%%'
          % (uniqueValue, len(testPixel[testPixel]),
             (1 - badPixel[badPixel].sum() / float(testPixel[testPixel].sum()))*100 ))

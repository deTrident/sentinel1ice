### TRAIN RANDOM FOREST BASED CLASSIFIER

import os, glob, pickle, gdal
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from config import get_env

# read configuration
env = get_env()
srcType = env['sourceType']
if srcType=='manual':
    ext = '_manual_classification.tif'
else:
    ext = '_reprojected_ice_chart.tif'
idir = env['outputDirectory']
classifierFilename = env['classifierFilename']
threads = env['numberOfThreads']
# set up parameters for training
trainProportion = 0.6
# listup reprojected ice charts
ifiles = sorted(glob.glob(idir+'*/*%s' % ext))
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
if srcType=='AARI':
    # exclude some ice codes (0:unclassified, 99:fast ice, 94,96:summer)
    gpi = ( np.isfinite(features_all.sum(axis=1)) * (iceCodes_all != 0)
            * (iceCodes_all != 99) * (iceCodes_all != 92) * (iceCodes_all != 94) )
elif srcType=='CIS':
    # exclude some ice codes (0:unclassified)
    gpi = ( np.isfinite(features_all.sum(axis=1)) * (iceCodes_all != 0) )
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
tuneIndices = trainIndices[:np.min([int((10000/env['stepSize'])**2), len(trainIndices)])]
tuneFeatures = features_all[tuneIndices]
tuneZones = iceCodes_all[tuneIndices]
grid = GridSearchCV(RandomForestClassifier(),
                    param_grid={'n_estimators':np.logspace(0, 9, 10, base=2, dtype=int).tolist(),
                                'max_features':['auto', 'sqrt', 'log2']},
                    n_jobs=threads, verbose=10)
grid.fit(tuneFeatures, tuneZones)
opt_params = {'max_features':grid.best_params_['max_features'],
              'n_estimators':grid.best_params_['n_estimators']}
from scipy.optimize import curve_fit
valid = [p['max_features']==opt_params['max_features'] for p in grid.cv_results_['params']]
x = np.array([p['n_estimators'] for p in grid.cv_results_['params']])[valid]
y = grid.cv_results_['mean_test_score'][valid]
def logFunction(x,p1,p2,p3,p4):
    return p1 + p2 * np.log(p3 * (x + p4))
popt, pcov = curve_fit(logFunction, x, y)
xi = np.arange(x[0],x[-1]+1)
thres = 0.001    # score improvements when increasing n_estimators by 1
opt_params['n_estimators'] = xi[np.argwhere(np.gradient(logFunction(xi, *popt)) <= thres).min()]
### train classifier
print('*** Training classifier: %d samples.' % len(trainIndices))
trainFeatures = features_all[trainIndices,:]
trainZones = iceCodes_all[trainIndices]
clf = RandomForestClassifier(**opt_params, n_jobs=threads, verbose=10)
clf.fit(trainFeatures, trainZones)
pickle.dump(clf, open(classifierFilename, "wb" ))
### test classifier
print('*** Testing classifier: %d samples.' % len(testIndices))
testFeatures = features_all[testIndices,:]
testZones = iceCodes_all[testIndices]
result = clf.predict(testFeatures)
print('classID    nSamples    accuracy')
for uniqueValue in np.unique(testZones):
    testPixel = (testZones == uniqueValue)
    badPixel = (result[testPixel] != uniqueValue)
    print('%7s    %8d     %6.3f%%'
          % (uniqueValue, len(testPixel[testPixel]),
             (1 - badPixel[badPixel].sum() / float(testPixel[testPixel].sum()))*100 ))

### TRAIN RANDOM FOREST BASED CLASSIFIER

import os, glob, pickle, gdal
import numpy as np
from sklearn.preprocessing import QuantileTransformer
from sklearn.decomposition import PCA
from scipy.cluster import vq
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from scipy.optimize import curve_fit
import scipy.ndimage as nd
import config as cfg


nSamplesForTuningHP = int((10000/cfg.stepSize)**2)

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
dist_from_boundary = 3
features_all = []
iceCodes_all = []
print('*** Importing files from:')
for li, ifile in enumerate(ifiles):
    print('[%d/%d] %s' % (li+1, len(ifiles), os.path.dirname(ifile)))
    npz = np.load(ifile.replace(ext, '_texture_features.npz'))
    tfsHH = npz['textureFeatures'].item()['HH']
    tfsHV = npz['textureFeatures'].item()['HV']
    iceCode = gdal.Open(ifile).ReadAsArray()
    for ic in np.unique(iceCode):
        valid = (nd.distance_transform_edt(iceCode==ic) > dist_from_boundary)
        features_all.append(np.vstack([tfsHH,tfsHV])[:,valid])
        iceCodes_all.append(iceCode[valid])
features_all = np.hstack(features_all).T
iceCodes_all = np.hstack(iceCodes_all).T

# generate sample mask for some ice codes
# 98:glacier, 99:undefined, 107:fast ice, 108:iceberg, 255:land
gpm = ( np.isfinite(features_all.sum(axis=1)) * (iceCodes_all != 98) * (iceCodes_all != 99)
        * (iceCodes_all != 107) * (iceCodes_all != 108) * (iceCodes_all != 255) )
gpi = np.nonzero(gpm)[0]

# modify sample mask via PCA-Kmeans
print('*** Filtering samples using PCA and K-means clustering.')
numberOfPC = np.ceil(np.sqrt(features_all.shape[1])).astype(np.int)
numberOfCluster = 10
thres = {0:1.0, 82:1.0, 83:0.8, 86:0.8, 95:0.8}
for ic in np.unique(iceCodes_all[gpm]):
    try:
        th = thres[ic]
    except:
        th = 0.8
    if th==1.0:
        continue
    v = (iceCodes_all[gpi]==ic)
    x = PCA(n_components=numberOfPC).fit_transform(
            QuantileTransformer(output_distribution='normal').fit_transform(features_all[gpi][v]))
    y = iceCodes_all[gpi][v]
    codeBook = vq.kmeans(x, numberOfCluster)[0]
    labelVec = vq.vq(x, codeBook)[0]
    w = np.array([(labelVec==l).sum() for l in range(numberOfCluster)]) / len(labelVec)
    numberOfClusterToUse = (np.cumsum(w[np.argsort(w)][::-1]) < th).sum() + 1
    bi = np.argsort(w)[:numberOfCluster-numberOfClusterToUse]
    bpi = gpi[v][np.array([lv in bi for lv in labelVec])]
    gpm[bpi] = False

# apply sample mask
features_all = features_all[gpm]
iceCodes_all = iceCodes_all[gpm]

### divide data into train/test set
test_size = (1. - cfg.maxNumberOfSamplesToTrain/len(iceCodes_all))
if test_size <= 0:
    test_size = 0.3
trainFeatures, testFeatures, trainZones, testZones = train_test_split(
    features_all, iceCodes_all, test_size=test_size)


### tune hyper-parameters
print('*** Tuning hyper-parameters.')
tuneFeatures = trainFeatures[:np.min([nSamplesForTuningHP, len(trainFeatures)])]
tuneZones = trainZones[:np.min([nSamplesForTuningHP, len(trainFeatures)])]
param_grid={'n_estimators':np.logspace(1, 6, 6, base=2, dtype=int).tolist(),
            'max_depth':np.logspace(1, 6, 6, base=2, dtype=int).tolist(),
            'max_features':['log2','sqrt'],
            'min_samples_leaf':np.logspace(0, 2, 3, base=2, dtype=int).tolist()}
grid = GridSearchCV(RandomForestClassifier(), param_grid=param_grid,
                    n_jobs=cfg.numberOfThreads, verbose=10)
grid.fit(tuneFeatures, tuneZones)
opt_params = {'n_estimators':grid.best_params_['n_estimators'],
              'max_depth':grid.best_params_['max_depth'],
              'max_features':grid.best_params_['max_features'],
              'min_samples_leaf':grid.best_params_['min_samples_leaf']}
valid = [    p['max_depth']==grid.best_params_['max_depth']
         and p['max_features']==grid.best_params_['max_features']
         and p['min_samples_leaf']==grid.best_params_['min_samples_leaf']
         for p in grid.cv_results_['params']]
x = np.array([p['n_estimators'] for p in grid.cv_results_['params']])[valid]
y = grid.cv_results_['mean_test_score'][valid]
def modelFunction(x, a, b, c, d, g):
    return ( (a-d) / ( (1+( ((x-x[0])/c)** b )) **g) ) + d
popt, pcov = curve_fit(modelFunction, x, y, maxfev=100000)
xi = np.arange(x[0],x[-1]+1)
thres = 0.001    # score improvements when increasing n_estimators by 1
opt_params['n_estimators'] = xi[np.argwhere(np.gradient(modelFunction(xi, *popt)) <= thres).min()]
valid = [    p['n_estimators']==grid.best_params_['n_estimators']
         and p['max_features']==grid.best_params_['max_features']
         and p['min_samples_leaf']==grid.best_params_['min_samples_leaf']
         for p in grid.cv_results_['params']]
x = np.array([p['max_depth'] for p in grid.cv_results_['params']])[valid]
y = grid.cv_results_['mean_test_score'][valid]
def modelFunction(x, a, b, c, d, g):
    return ( (a-d) / ( (1+( ((x-x[0])/c)** b )) **g) ) + d
popt, pcov = curve_fit(modelFunction, x, y, maxfev=100000)
xi = np.arange(x[0],x[-1]+1)
thres = 0.001    # score improvements when increasing max_depth by 1
opt_params['max_depth'] = xi[np.argwhere(np.gradient(modelFunction(xi, *popt)) <= thres).min()]

### train classifier
print('*** Training classifier: %d samples.' % len(trainZones))
clf = RandomForestClassifier(**opt_params, n_jobs=cfg.numberOfThreads, verbose=10)
clf.fit(trainFeatures, trainZones)
pickle.dump(clf, open(cfg.classifierFilename, "wb" ))

### test classifier
clf = pickle.load(open(cfg.classifierFilename, "rb" ))
print('*** Testing classifier: %d samples.' % len(testZones))
result = clf.predict(testFeatures)
print('classID    nSamples    accuracy')
for uniqueValue in np.unique(testZones):
    testPixel = (testZones == uniqueValue)
    badPixel = (result[testPixel] != uniqueValue)
    print('%7s    %8d     %6.3f%%'
          % (uniqueValue, len(testPixel[testPixel]),
             (1 - badPixel[badPixel].sum() / float(testPixel[testPixel].sum()))*100 ))

### TRAIN RANDOM FOREST BASED CLASSIFIER

import os, glob, pickle, gdal
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from scipy.optimize import curve_fit
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

# exclude dark pixels in some ice classes by threasholding
sigma0HH_all = []
sigma0HV_all = []
for li, ifile in enumerate(ifiles):
    sigma0HH_all.append(Nansat(ifile.replace(ext, '_sigma0_HH_denoised.tif'))[1].flatten())
    sigma0HV_all.append(Nansat(ifile.replace(ext, '_sigma0_HV_denoised.tif'))[1].flatten())
sigma0HH_all = np.hstack(sigma0HH_all).T
sigma0HV_all = np.hstack(sigma0HV_all).T
sigma0HH_all = sigma0HH_all[gpi]
sigma0HV_all = sigma0HV_all[gpi]
bpi = (iceCodes_all==83) * (sigma0HV_all < 10**(-25/10))
gpi = np.invert(bpi)
features_all = features_all[gpi]
iceCodes_all = iceCodes_all[gpi]
sigma0HH_all = sigma0HH_all[gpi]
sigma0HV_all = sigma0HV_all[gpi]
bpi = (iceCodes_all==86) * (sigma0HV_all < 10**(-25/10))
gpi = np.invert(bpi)
features_all = features_all[gpi]
iceCodes_all = iceCodes_all[gpi]
sigma0HH_all = sigma0HH_all[gpi]
sigma0HV_all = sigma0HV_all[gpi]
bpi = (iceCodes_all==95) * (sigma0HV_all < 10**(-22/10))
gpi = np.invert(bpi)
features_all = features_all[gpi]
iceCodes_all = iceCodes_all[gpi]
sigma0HH_all = sigma0HH_all[gpi]
sigma0HV_all = sigma0HV_all[gpi]

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

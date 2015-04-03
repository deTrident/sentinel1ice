import os
import glob
from multiprocessing import Pool

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

import Image

from sklearn import svm

import pickle

def clf_predict(inputData):
    return clf.predict(inputData)


idir = '/files/sentinel1a/odata/'
myZonesSuffix = '_my_zones.png'
zoneColors = [0, 255]
n_threads = 6
svmFileName = 'svm_test0.pickle'

ifilesHH = sorted(glob.glob(idir + '*_HH_har_norm.npz'))
allData = []
goodFiles = []
for ifileHH in ifilesHH:
    ifileHV = ifileHH.replace('HH', 'HV')
    ifileMyZones = ifileHH.replace('_HH_har_norm.npz', myZonesSuffix)
    if not os.path.exists(ifileHV):
        continue
    if not os.path.exists(ifileMyZones):
        continue
    print ifileHH, ifileHV, ifileMyZones
    hhTF = np.load(ifileHH)['tfsNorm']
    hvTF = np.load(ifileHV)['tfsNorm']
    # read the image with my classification
    myZonesImg = np.array(Image.open(ifileMyZones))
    # resize from GIMP resolution back to original size
    myZonesImg = myZonesImg[::8, ::8, :][:hhTF.shape[1], :hhTF.shape[2]]
    myZones = np.zeros((myZonesImg.shape[0], myZonesImg.shape[1])) + np.nan
    for zc in zoneColors:
        # find non transparent pixels
        # with defined color (whiate, or gray, or black)
        gpi = (
               (myZonesImg[:,:,0] == zc ) *
               (myZonesImg[:,:,1] == zc ) *
               (myZonesImg[:,:,2] == zc ) *
               (myZonesImg[:,:,3] == 255)
               )
        myZones[gpi] = zc

    # stack HH/HV textures and zones
    imgData = np.vstack([hhTF, hvTF, myZones[None]])
    # reshape into stackable 2D matrix
    imgData = imgData.reshape(27, hhTF.shape[1]*hhTF.shape[2])

    # append data from many images
    allData.append(imgData)
    goodFiles.append(ifileHH)

# stack data from all images into 27 x n_pixes array
allData = np.hstack(allData)

gpi = np.isfinite(allData.sum(axis=0))
allDataGood = allData[:, gpi]

# random indeces
randIndeces = np.random.permutation(allDataGood.shape[1])
print len(randIndeces)
# training and testing data
maxSize = 1000
trnIndeces = randIndeces[:maxSize]
tstIndeces = randIndeces[maxSize:maxSize+maxSize]

trnTF = allDataGood[:26, trnIndeces]
trnZones = allDataGood[26, trnIndeces]

tstTF = allDataGood[:26, tstIndeces]
tstZones = allDataGood[26, tstIndeces]

# train SVM
print 'Train SVM'
clf0 = svm.SVC(C=1.0, gamma=0.1)
clf0.fit(trnTF.T, trnZones)

# save SVM into file
pickle.dump(clf0, open(svmFileName, "wb" ))

# load SVM from file
clf = pickle.load(open(svmFileName, "rb" ))

# test SVM on small independent subsample
print 'Test on independent sample'
svmZones = clf_predict(tstTF.T)

diff = tstZones - svmZones
print len(diff[diff != 0]) / float(len(diff))

# apply SVM to all data for testing (in threads)
print 'Apply SVM to %d vectors' % allDataGood.shape[1]
pool = Pool(n_threads)

# split good data into chunks for parallel processing
chunkSize = 100000
allDataGoodChunks = [allDataGood[:26, i:i+chunkSize].T for i in range(0, allDataGood.shape[1], chunkSize)]

# run parallel processing of all data with SVM
svmZonesGood = pool.map(clf_predict, allDataGoodChunks)

# join results back from the queue and insert into full matrix
svmZonesGood = np.hstack(svmZonesGood)
svmZonesAll = np.zeros(allData.shape[1]) + np.nan
svmZonesAll[gpi] = svmZonesGood

# convert to results to processed images
startPix = 0
for ifileHH in goodFiles:
    hhTF = np.load(ifileHH)['tfsNorm']
    imgSize = hhTF.shape[1] * hhTF.shape[2]
    print hhTF.shape[1], hhTF.shape[2], imgSize
    svmZones = svmZonesAll[startPix:startPix+imgSize].reshape(hhTF.shape[1], hhTF.shape[2])
    ofileSVM = ifileHH.replace('_HH_har_norm.npz', '_svm_zones.png')
    plt.imsave(ofileSVM, svmZones)
    startPix += imgSize

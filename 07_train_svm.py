import os, glob, pickle
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import svm
from sar2ice import apply_svm

idir = ( os.path.abspath(os.getcwd()+'/../shared/test_data/sentinel1a_l1')
         +'/odata_FramStrait_TFs/' )
myZonesSuffix = '_my_zones.png'
zoneColors = [0, 255]
n_threads = 6
svmFile = 'svm.pickle'

ifilesHH = sorted(glob.glob(idir + '*_HH_har_norm.npz'))
allData = []
for ifileHH in ifilesHH:
    ifileHV = ifileHH.replace('HH','HV')
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

# stack data from all images into 27 x n_pixes array
allData = np.hstack(allData)

gpi = np.isfinite(allData.sum(axis=0))
allDataGood = allData[:, gpi]

# random indeces
randIndeces = np.random.permutation(allDataGood.shape[1])
print len(randIndeces)
# training and testing data
maxSize = 100000
trnIndeces = randIndeces[:maxSize]
tstIndeces = randIndeces[maxSize:maxSize+maxSize]

trnTF = allDataGood[:26, trnIndeces]
trnZones = allDataGood[26, trnIndeces]

tstTF = allDataGood[:26, tstIndeces]
tstZones = allDataGood[26, tstIndeces]

# train SVM
print 'Train SVM'
clf = svm.SVC(C=1.0, gamma=0.1)
clf.fit(trnTF.T, trnZones)

# save SVM into file
pickle.dump(clf, open(svmFile, "wb" ))

# test SVM on small independent subsample
print 'Test on independent sample'
svmZones = clf.predict(tstTF.T)

diff = tstZones - svmZones
print len(diff[diff != 0]) / float(len(diff))

# apply SVM to all data for testing (in threads)
ifilesHH = sorted(glob.glob(idir + '*_HH_har_norm.npz'))
for ifileHH in ifilesHH:
    ifileHV = ifileHH.replace('HH', 'HV')
    if not os.path.exists(ifileHV):
        continue
    hhTF = np.load(ifileHH)['tfsNorm']
    hvTF = np.load(ifileHV)['tfsNorm']
    # stack HH/HV textures and zones
    tfs = np.vstack([hhTF, hvTF])

    svmMap = apply_svm(tfs, svmFile, 6)
    ofileSVM = ifileHH.replace('_HH_har_norm.npz', '_svm_zones.png')
    plt.imsave(ofileSVM, svmMap)

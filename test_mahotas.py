from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import wiener
from scipy.ndimage.interpolation import zoom

import mahotas

from zoning import *

def call_haralick(inputTuple):
    haralick = mahotas.features.haralick(inputTuple[0], inputTuple[1])
    if haralick.shape != (4, 13):
        haralick = np.zeros((4, 13)) + np.nan
    return haralick

pol = 'HH'
sigma0_max = {'HH': 0,   'HV': -14}
sigma0_min = {'HH': -15, 'HV': -26}
stp = 8
pool = Pool(6)
prefix = 'mahotashr2'

ifile = 'S1A_EW_GRDM_1SDH_20150207T151223_20150207T151323_004519_0058C6_9A73.sigma0_%s.npz'
ifile = 'S1A_EW_GRDM_1SDH_20150119T071200_20150119T071300_004237_005272_41A2.sigma0_%s.npz'

wsws = [32]#[16, 32, 64]
ll = [64]#[32, 64, 128]

for pol in ['HH', 'HV']:
    sigma0raw = np.load(ifile % pol)['sigma0_%s' % pol]
    sigma0raw = 10 * np.log10(sigma0raw)
    #plt.imsave(ifile % pol + '.jpg', sigma0raw, vmin=sigma0_min[pol], vmax=sigma0_max[pol], cmap='gray')

    for ws in wsws:
        for l in ll:
            ofile = '%s_%03d_%03d_%s_' % (prefix, ws, l, pol)
            # convert t integer leves
            sigma0 = (l * (sigma0raw - sigma0_min[pol]) / (sigma0_max[pol] - sigma0_min[pol])).astype('uint8')
            sigma0[sigma0 < 1] = 1
            sigma0[sigma0 > l] = l
            if pol == 'HV':
                sigma0[:, 2990:3040] = 0
                sigma0[:, 6980:7030] = 0
                sigma0[:, 8840:8900] = 0

            sigma0[:, :100] = 0
            sigma0[:, 10000:] = 0
            sigma0[np.isinf(sigma0raw)] = 0
            sigma0[np.isnan(sigma0raw)] = 0

            #plt.imshow(sigma0, vmin=0, vmax=l)
            #plt.savefig(ofile + 'sigma0.png')
            #plt.close()

            harList = []
            for r in range(0, sigma0.shape[0]-ws-1, stp):
                print ws, l, r
                # collect all subimages in the row
                subImgs = [(sigma0[r:r+ws, c:c+ws], True) for c in range(0, sigma0.shape[1]-ws-1, stp)]
                # apply haralic (in parallel)
                harRow = pool.map(call_haralick, subImgs)
                harList.append(np.array(harRow))
                if np.array(harRow).shape != (len(subImgs),4,13):
                    raise

            # convrt lists to arrays
            harImage = np.array(harList)
            # calculate directional mean
            harImageAnis = harImage.mean(axis=2)
            # make images to be on the first dimension
            harImageAnis = np.swapaxes(harImageAnis.T, 1, 2)
            # save each TFin a PNG
            for i, harImg in enumerate(harImageAnis):
                plt.imsave(ofile+'har%02d.png' % i, harImg)

            # apply PCA
            pcs = pca(harImageAnis, pcNumber=13, oPrefix=ofile)
            np.savez_compressed(ofile + 'haralick.npz', harImageAnis=harImageAnis)

#%cpaste
for ws in wsws:
    for l in ll:
        harImages = []
        for pol in ['HH', 'HV']:
            ifile = '%s_%03d_%03d_%s_haralick.npz' % (prefix, ws, l, pol)
            harImages.append(np.load(ifile)['harImageAnis'])

        ofile = '%s_%03d_%03d_COMB_' % (prefix, ws, l)
        print ofile
        harImages = np.vstack(harImages)

        # mask bad data on input images (for stp=8)
        harImages[:, :, 366:376] = np.nan
        harImages[:, :, 602:611] = np.nan
        harImages[:, :, 864:876] = np.nan
        harImages[:, :, 1099:1109] = np.nan

        # apply PCA
        pcs = pca(harImages, pcNumber=13, oPrefix=ofile, maxVal=4)

        # mask edges as nan
        #pcs[:, :, 180:190] = np.nan
        #pcs[:, :, 430:440] = np.nan
        #pcs[:, :, 548:554] = np.nan
        #pcs[:, :, 636:] = np.nan


        kPref = '4x10tf_'
        zoneMap = kmeans(pcs[:4], 10, ofile+kPref, True, False)

#%cpaste
# add supervised classification

combZoneFiles = glob.glob(prefix + '*COMB_' + kPref + '*.npy')
for combZoneFile in combZoneFiles:
    print combZoneFile
    mask = plt.imread('mask.png')
    zones = np.load(combZoneFile)
    zoomFactor = np.array(zones.shape) / np.array(mask.shape, 'float64')
    mask = zoom(mask, zoomFactor)

    # get super classes
    waterMask = np.round(mask) == 0
    iceMask = np.round(mask * 255) == 186

    newZones = np.zeros_like(zones) + np.nan
    uz = np.unique(zones[np.isfinite(zones)])
    print len(uz)
    icek = 0
    waterk = 0
    for z in uz:
        print z
        zMask = (zones == z)
        interceptWater = waterMask * zMask
        interceptIce = iceMask * zMask
        if len(interceptWater[interceptWater]) > len(interceptIce[interceptIce]):
            newZones[zMask] = icek
            icek += 1

        if len(interceptWater[interceptWater]) < len(interceptIce[interceptIce]):
            newZones[zMask] = 30 + waterk
            waterk += 1

    plt.imsave(combZoneFile + 'reclas.png',newZones )

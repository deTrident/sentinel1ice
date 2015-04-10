import os
from multiprocessing import Pool
import glob

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage.filters import gaussian_filter

from sklearn.cluster import KMeans

import mahotas


from sentinel1image import Sentinel1Image

def clean_zones(zones, minSegmentSize):
    ''' Remove small zones and replace with nearest neigbour'''
    # bad zones mask
    badMask = zones == -1

    # indices of all non-zero zones
    zIndices = np.unique(zones)
    zIndices = zIndices[zIndices >= 0]
    structure = np.ones((3,3)) # for labeling

    # split spatially separate single zones into to multiple zones
    lblCounter = 0
    # matrix for all spatially separate zones (-1 masks bad data)
    zonesAll = np.zeros_like(zones) - 1
    for zi in zIndices:
        # find zone
        mask = zones == zi
        # split spatially
        labels, nl = ndimage.label(mask, structure)
        # add unique numbers
        labels[labels > 0] += lblCounter
        # add zones to new matrix
        zonesAll += labels
        lblCounter += nl

    # find areas of all zones
    zAllIndeces = np.unique(zonesAll)
    zAllIndeces = zAllIndeces[zAllIndeces >= 0]
    zAllAreas = ndimage.sum(np.ones_like(zones), zonesAll, zAllIndeces)

    # set zones with small areas to -1
    for zai in zAllIndeces[zAllAreas < minSegmentSize]:
        zonesAll[zonesAll == zai] = -1

    # fill small segments with values from nearest neighbours
    invalid_cell_mask = zonesAll == -1
    indices = ndimage.distance_transform_edt(invalid_cell_mask, return_distances=False, return_indices=True)
    zonesClean = zones[tuple(indices)]

    # mask bad values with 0
    zonesClean[badMask] = -1

    return zonesClean

def get_zones(inputArray, borderSize, gaussRadius, nSegments):
    ''' Perfrom segmentation of a subimage '''
    # get X,Y coordinates centered at 0 and normed to STD
    x,y = np.mgrid[-1.75 : 1.75 : complex(0, inputArray.shape[1]),
                   -1.75 : 1.75 : complex(0, inputArray.shape[2])]
    subimgs = [x, y]

    # pre-process values in input array
    for subimg in inputArray:
        # filter subimage
        subimgGaus = gaussian_filter(subimg, gaussRadius)
        # center on mean and normalize to STD
        subimgNorm = (subimgGaus - np.nanmean(subimgGaus)) / np.nanstd(subimgGaus)
        subimgs.append(subimgNorm)

    # stack X, Y and sigma0 and reshape from 3D cube to 2D matrix
    subimgs = np.array(subimgs)
    subimgs = subimgs.reshape(2 + inputArray.shape[0],
                               inputArray.shape[1]*inputArray.shape[2])

    # matrix for segments from subimage
    # -1 masks invalid data
    zones = np.zeros(inputArray.shape[1]*inputArray.shape[2], 'int32') - 1

    # select good pixels
    gpi = np.isfinite(subimgs.sum(axis=0))
    # if no good pixels, return empty zones, else do segmentation
    if len(subimgs[0][gpi]) > 0:
        # perform KMeans clustering
        zones[gpi] = KMeans(n_clusters=nSegments).fit_predict(subimgs.T[gpi])

    # return 2D map of zones
    zones = zones.reshape(inputArray.shape[1], inputArray.shape[2])

    return zones

def get_textures_in_segments(inputArray, zones, zIndices, vmins, vmaxs, l):
    ''' Calculate texture features in segments'''
    # calculate TF in all segments
    textures = []
    for z in zIndices:
        # skip segments with no data
        if z < 0:
            continue

        # mask only that segment
        mask = (zones == z)

        # calculate Harlick textue features
        haralick = []
        for subimg, vmin, vmax in zip(inputArray, vmins, vmaxs):
            # convert to gray levels
            imgMahotas = (1 + l * (subimg - vmin) / (vmax - vmin))
            # replace outliers
            imgMahotas[imgMahotas < 1] = 1
            imgMahotas[imgMahotas > l] = l
            # mask data outside segment
            imgMahotas[zones != z] = 0
            # get texture features
            features = mahotas.features.haralick(imgMahotas.astype('uint8'), True).mean(axis=0)
            haralick.append(features)

        textures.append(np.hstack(haralick))

    return np.array(textures)

def get_zones_and_tf(inputData):
    ''' Perfrom segmentation of a subimage and calculate texture features'''
    # unpack data from tuple
    (cc, inputArray,
     borderSize, gaussRadius, nSegments, minSegmentSize,
     vmins, vmaxs, l) = inputData
    print 'Process column ', cc

    # add singleton 3rd dimension
    if len(inputArray.shape) == 2:
        inputArray = inputArray[None]

    # get zones from input array
    zones = get_zones(inputArray, borderSize, gaussRadius, nSegments)

    # remove too small segments
    zones = clean_zones(zones, minSegmentSize)

    # central part of the zones to be used further
    zonesCenter = zones[borderSize:-borderSize, borderSize:-borderSize]
    # get list of zones for which TF should be calculated
    zIndices = np.unique(zonesCenter)

    # get texture features in each segment
    textures = get_textures_in_segments(inputArray, zones, zIndices, vmins, vmaxs, l)

    #change numbering of zones to match indices of textures
    zonesReturn = np.zeros_like(zonesCenter)
    zn = 0
    for zi in zIndices:
        zonesCenter[zonesCenter == zi] = zn
        zn += 1

    return zonesCenter, textures

def get_segmented_tf(inputArray, windowSize=200,
                                    borderSize=50,
                                    gaussRadius=3,
                                    nSegments=20,
                                    minSegmentSize=500,
                                    vmins=[-15,-22],
                                    vmaxs=[0,-14],
                                    l=64,
                                    threads=2):
    ''' Split input image into segments and get texture feature in segments'''

    # add singleton 3rd dimension
    if len(inputArray.shape) == 2:
        inputArray = inputArray[None]

    stp = windowSize - borderSize - borderSize

    bands = range(0, inputArray.shape[0])
    rows = range(0, inputArray.shape[1]-stp, stp)
    cols = range(0, inputArray.shape[2]-stp, stp)

    # image with segments
    segments = np.zeros((inputArray.shape[1], inputArray.shape[2]), 'int32') - 1

    pool = Pool(threads)

    zoneCounter = 0
    textures = []
    for rr in rows:
        print 'Process row ', rr
        subArrays = []
        # collect subimages along the row into a list
        for cc in cols:
            # pack sub-image and auxiliarry data into tuples
            subArrays.append((cc,
                              inputArray[:, rr:rr+windowSize, cc:cc+windowSize],
                              borderSize,
                              gaussRadius,
                              nSegments,
                              minSegmentSize,
                              vmins, vmaxs, l))

        # for debug only
        #rowZonesTFs = []
        #for subArray in subArrays:
        #    rowZonesTF = get_zones_and_tf(subArray)
        #    rowZonesTFs.append(rowZonesTF)
        #    import ipdb; ipdb.set_trace()

        # run segmentation of subimages in that row in multiple threads
        rowZonesTFs = pool.map(get_zones_and_tf, subArrays)

        # insert zones into global matrix with zones
        for ic, cc in enumerate(cols):
            # get segmented image
            zones = rowZonesTFs[ic][0]
            tf = rowZonesTFs[ic][1]

            # set unique numbering of zones
            zonesMax = zones.max()
            zones += zoneCounter
            zoneCounter += zonesMax + 1

            # put center of zones data into global matrix with zones
            segments[rr+borderSize:rr+windowSize-borderSize,
                     cc+borderSize:cc+windowSize-borderSize] = zones

            # append textures from that subimage
            textures.append(tf)
    textures = np.vstack(textures)
    return segments, textures


# find input files
idir = '/files/sentinel1a/'
odir = '/files/sentinel1a/odata/'
ifiles = sorted(glob.glob(idir + '*.SAFE'))


## parameers for segmetation
windowSize  = 200
borderSize = 50
gaussRadius = 3
nSegments = 20
minSegmentSize = 500

## parameters for Haralick texture features computation
vmins=[-15, -22]
vmaxs=[  0, -14]
l = 64

# multiprocessing
threads = 6

for ifilepath in [ifiles[0]]:
    ifile = os.path.split(ifilepath)[1]
    print ifile
    sigma0HHHV = []
    for pol in ['HH', 'HV']:
        # set output file namew
        ofile = '%s_%s_' % (os.path.join(odir, ifile), pol)
        ofileNPZ = ofile + 'seghar.npz'

        # skip processing already extisting files
        if os.path.exists(ofileNPZ):
            continue

        # read data from input file
        s1i = Sentinel1Image(idir + ifile)
        s1i.crop(2000, 2000, 700, 500)  # for testing only
        print 'Read sigma0_%s from %s' % (pol, ifile)
        sigma0 = s1i['sigma0_%s' % pol]
        sigma0HHHV.append(sigma0)


    sigma0HHHV = np.array(sigma0HHHV)
    segments, textures = get_segmented_tf(sigma0HHHV,
                                windowSize=windowSize,
                                borderSize=borderSize,
                                gaussRadius=gaussRadius,
                                nSegments=nSegments,
                                minSegmentSize=minSegmentSize,
                                vmins=vmins,
                                vmaxs=vmaxs,
                                l=l,
                                threads=threads)

    textures2D = textures.T[:, segments]
    textures2D[:, segments == -1] = np.nan

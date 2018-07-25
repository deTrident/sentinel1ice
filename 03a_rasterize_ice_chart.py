### RASTERIZE THE AARI ICE CHART AND REPROJECT IT INTO THE S-1 IMAGE GEOMETRY

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, zipfile, tarfile, shutil, gdal, ogr
import numpy as np
from nansat import Nansat
from config import get_env
from sar2ice import julian_date, colorDict

# read configuration
env = get_env()
sourceType = env['sourceType']
# listup denoised images and ice charts
denoisedImages = sorted(glob.glob(get_env()['outputDirectory'] + '*/*_denoised_gamma0_HH.tif'))
iceChartFiles = sorted(glob.glob(env['iceChartDirectory'] + '/*.zip'))
# make pair
if sourceType=='AARI':
    iceChartPubDateInJD = [julian_date(f.split('/')[-1].split('_')[2][:8]+'T235959') for f in iceChartFiles]
elif sourceType=='CIS':
    iceChartPubDateInJD = [julian_date(f.split('/')[-1].split('_')[2][:8]+'T180000') for f in iceChartFiles]
imageAcqDateInJD = [julian_date(f.split('/')[-1][17:32]) for f in denoisedImages]
list2process = []
for li,iJD in enumerate(imageAcqDateInJD):
    diffJD = iJD - iceChartPubDateInJD
    closestDateDiffArg = np.argmin(np.abs(diffJD))
    if (diffJD[closestDateDiffArg] > -3) * (diffJD[closestDateDiffArg] < 0):
        list2process.append((denoisedImages[li], iceChartFiles[closestDateDiffArg]))
# process each pair
for ifile, iceChartFile in list2process:
    ofile = ifile.replace('_denoised_gamma0_HH.tif', '_reprojected_ice_chart.tif')
    if os.path.exists(ofile):
        continue
    print(ofile)
    unzipDir = (os.path.dirname(ofile)+'/'+iceChartFile.split('/')[-1][:-4])
    if iceChartFile.split('.')[-1]=='zip':
        zipfile.PyZipFile(iceChartFile).extractall(path=unzipDir)
    elif iceChartFile.split('.')[-1]=='tar':
        tarfile.open(iceChartFile).extractall(path=unzipDir)
    iVector = ogr.Open(glob.glob(unzipDir+'/*.shp')[0])
    iLayer = iVector.GetLayer()
    oVector = ogr.GetDriverByName('MEMORY').CreateDataSource('memData')
    oLayer = oVector.CopyLayer(iLayer, 'classID')
    fidef = ogr.FieldDefn('classID', ogr.OFTReal)
    oLayer.CreateField(fidef)
    for ft in oLayer:
        maxInd = np.argmax([ft.GetFieldAsInteger(fieldName) for fieldName in ['CA', 'CB', 'CC']])
        S = [ft.GetFieldAsInteger(fieldName) for fieldName in ['SA', 'SB', 'SC']][maxInd]
        CT = ft.GetFieldAsInteger('CT')
        if (S==99) and (CT==40):
            S = 94
        elif (S==99) and (CT==80):
            S = 96
        ft.SetField('classID', S)
        oLayer.SetFeature(ft)
    fp_GAMMA0 = gdal.Open(ifile)
    GAMMA0 = fp_GAMMA0.ReadAsArray()
    fp_classID = gdal.Open(ifile)
    gdal.RasterizeLayer(fp_classID, [1], oLayer, options=["ATTRIBUTE=classID"])
    classID = fp_classID.ReadAsArray()
    classID[classID==GAMMA0] = 0
    classID[np.isnan(classID)] = 0
    if classID.sum()==0:
        continue
    nansatObjGamma0 = Nansat(ifile)
    nansatObjIceChart = Nansat(array=classID, domain=nansatObjGamma0)
    nansatObjIceChart.export(ofile, bands=[1], driver='GTiff')
    rgb = np.zeros((classID.shape[0], classID.shape[1], 3), 'uint8')
    for k in colorDict[sourceType].keys():
        rgb[classID==k,:] = colorDict[sourceType][k]
    plt.imsave(ofile.replace('_reprojected_ice_chart.tif', '_reprojected_ice_chart_color.png'), rgb)

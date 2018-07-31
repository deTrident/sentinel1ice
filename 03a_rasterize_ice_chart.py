### RASTERIZE THE AARI ICE CHART AND REPROJECT IT INTO THE S-1 IMAGE GEOMETRY

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, zipfile, shutil, gdal, ogr
import numpy as np
from nansat import Nansat
import config as cfg
from sar2ice import julian_date, colorDict

# read configuration
# listup denoised images and ice charts
denoisedImages = sorted(glob.glob(cfg.outputDirectory + '*/*_denoised_gamma0_HH.tif'))
iceChartFiles = sorted(glob.glob(cfg.iceChartDirectory + '%s/*.zip' % cfg.sourceType))
# make pair
if cfg.sourceType=='AARI':
    iceChartPubDateInJD = [julian_date(f.split('/')[-1].split('_')[2][:8]+'T000000') for f in iceChartFiles]
elif cfg.sourceType=='NIC':
    iceChartPubDateInJD = [julian_date('20'+f.split('/')[-1][6:12]+'T000000') for f in iceChartFiles]
imageAcqDateInJD = [julian_date(f.split('/')[-1][17:32]) for f in denoisedImages]
list2process = []
for li,iJD in enumerate(imageAcqDateInJD):
    diffJD = iJD - iceChartPubDateInJD
    closestDateDiffArg = np.argmin(np.abs(diffJD))
    if (diffJD[closestDateDiffArg] > -3) * (diffJD[closestDateDiffArg] < 1):
        list2process.append((denoisedImages[li], iceChartFiles[closestDateDiffArg]))
# process each pair
for ifile, iceChartFile in list2process:
    ofile = ifile.replace('_denoised_gamma0_HH.tif', '_reprojected_%s.tif' % cfg.sourceType)
    if os.path.exists(ofile):
        continue
    print(ofile)
    unzipDir = (os.path.dirname(ofile)+'/'+iceChartFile.split('/')[-1][:-4])
    if iceChartFile.split('.')[-1]=='zip':
        zipfile.PyZipFile(iceChartFile).extractall(path=unzipDir)
    iVector = ogr.Open(glob.glob(unzipDir+'/*.shp')[0])
    iLayer = iVector.GetLayer()
    oVector = ogr.GetDriverByName('MEMORY').CreateDataSource('memData')
    oLayer = oVector.CopyLayer(iLayer, 'classID')
    fidef = ogr.FieldDefn('classID', ogr.OFTReal)
    oLayer.CreateField(fidef)
    for li, ft in enumerate(oLayer):
        POLY_TYPE = ft.GetFieldAsString('POLY_TYPE')
        if POLY_TYPE=='W':
            S = 0
        elif POLY_TYPE=='I':
            C = np.array([ft.GetFieldAsInteger(fieldName) for fieldName in ['CA', 'CB', 'CC']])
            S = np.array([ft.GetFieldAsInteger(fieldName) for fieldName in ['SA', 'SB', 'SC']])
            F = np.array([ft.GetFieldAsInteger(fieldName) for fieldName in ['FA', 'FB', 'FC']])
            maxInd = np.argwhere(C==np.max(C)).flatten()
            if (C==np.array([-9,-9,-9])).all():
                vInd = np.argwhere(S==np.max(S)).flatten()[-1]
            else:
                vInd = np.argwhere(C==np.max(C)).flatten()[-1]
            S = S[vInd]
            F = F[vInd]
            if S==99 and F==8:
                S = 99 + 8    # fast ice
            if S==98 and F==10:
                S = 98 + 10    # iceberg
            CT = ft.GetFieldAsInteger('CT')
            if CT==1:
                S = 1    # open water
        else:
            continue
        ft.SetField('classID', int(S))
        oLayer.SetFeature(ft)
    fp_GAMMA0 = gdal.Open(ifile)
    GAMMA0 = fp_GAMMA0.ReadAsArray()
    fp_classID = gdal.Open(ifile)
    gdal.RasterizeLayer(fp_classID, [1], oLayer, options=["ATTRIBUTE=classID"])
    classID = fp_classID.ReadAsArray()
    classID[classID==GAMMA0] = 99
    classID[np.isnan(classID)] = 99
    nansatObjGamma0 = Nansat(ifile)
    nansatObjIceChart = Nansat(array=classID, domain=nansatObjGamma0)
    nansatObjIceChart.export(ofile, bands=[1], driver='GTiff')
    rgb = np.zeros((classID.shape[0], classID.shape[1], 3), 'uint8')
    for k in colorDict.keys():
        rgb[classID==k,:] = colorDict[k]
    plt.imsave(ofile.replace('.tif', '.png'), rgb)

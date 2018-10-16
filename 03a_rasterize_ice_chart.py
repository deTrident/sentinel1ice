### RASTERIZE AND REPROJECT ICE CHART INTO S-1 IMAGE GEOMETRY

import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, zipfile, shutil, gdal, ogr
import numpy as np
from nansat import Nansat
import config as cfg
from sar2ice import modifiedJulianDate2000, colorDict, add_colortable

# read configuration
# listup denoised images and ice charts
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/*_sigma0_HH_denoised.tif'))
if (cfg.minDate!=None) and (cfg.maxDate!=None):
    ifiles = [f for f in ifiles
              if cfg.minDate <= os.path.split(f)[-1][17:25] <= cfg.maxDate]
iceChartFiles = sorted(glob.glob(cfg.iceChartDirectory + '%s/*.zip' % cfg.sourceType))
# make pair
if cfg.sourceType=='AARI':
    # AARI ice charts of Jun-Sep do not contain sufficient SoDs
    iceChartFiles = [f for f in iceChartFiles
                     if (   (f.split('/')[-1].split('_')[2][4:8] < '0601')
                         or (f.split('/')[-1].split('_')[2][4:8] > '0930'))]
    iceChartPubDateInJD = [modifiedJulianDate2000(f.split('/')[-1].split('_')[2][:8]+'T000000')
                           for f in iceChartFiles]
elif cfg.sourceType=='NIC':
    iceChartPubDateInJD = [modifiedJulianDate2000('20'+f.split('/')[-1][6:12]+'T000000')
                           for f in iceChartFiles]
imageAcqDateInJD = [modifiedJulianDate2000(f.split('/')[-1][17:32]) for f in ifiles]
list2process = []
for li,iJD in enumerate(imageAcqDateInJD):
    diffJD = iJD - iceChartPubDateInJD
    closestDateDiffArg = np.argmin(np.abs(diffJD))
    if cfg.sourceType=='AARI':
        if (diffJD[closestDateDiffArg] > -2) * (diffJD[closestDateDiffArg] < +1):
            list2process.append((ifiles[li], iceChartFiles[closestDateDiffArg]))
    elif cfg.sourceType=='NIC':
        if (diffJD[closestDateDiffArg] > -3) * (diffJD[closestDateDiffArg] < +2):
            list2process.append((ifiles[li], iceChartFiles[closestDateDiffArg]))

# process each pair
for ifile, iceChartFile in list2process:
    ofile = ifile.replace('_sigma0_HH_denoised.tif', '_reprojected_%s.tif' % cfg.sourceType)
    if os.path.exists(ofile) and cfg.force!=True:
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
            CC = 0    # color code for ice free
        elif POLY_TYPE=='I':
            CT = ft.GetFieldAsInteger('CT')
            if CT >= cfg.minCT:
                C = np.array([ft.GetFieldAsInteger(fieldName) for fieldName in ['CA', 'CB', 'CC']])
                S = np.array([ft.GetFieldAsInteger(fieldName) for fieldName in ['SA', 'SB', 'SC']])
                F = np.array([ft.GetFieldAsInteger(fieldName) for fieldName in ['FA', 'FB', 'FC']])
                if (C==np.array([-9,-9,-9])).all():
                    vInd = np.argwhere(S==np.max(S)).flatten()[0]
                else:
                    vInd = np.argwhere(C==np.max(C)).flatten()[0]
                S = S[vInd]
                CC = S
                F = F[vInd]
                if S==99 and F==8:
                    CC = 99 + 8    # color code for fast ice
                if S==98 and F==10:
                    CC = 98 + 10    # color code for iceberg
                CT = ft.GetFieldAsInteger('CT')
            else:
                CC = 2    # color code for bergy water
            if CT==1:
                CC = 1    # color code for open water
            if CT==98:
                CC = 0    # color code for ice free
        ft.SetField('classID', int(CC))
        oLayer.SetFeature(ft)
    sigma0 = gdal.Open(ifile).ReadAsArray()
    fp_classID = gdal.Open(ifile)
    gdal.RasterizeLayer(fp_classID, [1], oLayer, options=["ATTRIBUTE=classID"])
    classID = fp_classID.ReadAsArray()
    classID[classID==sigma0] = 255
    classID[np.isnan(classID)] = 99
    nansatObjSigma0 = Nansat(ifile)
    nansatObjIceChart = Nansat.from_domain(array=classID.astype(np.uint8), domain=nansatObjSigma0)
    nansatObjIceChart.set_metadata(nansatObjSigma0.get_metadata())
    nansatObjIceChart.set_metadata('entry_title', 'REPROJECTED_%s_ICE_CHART' % cfg.sourceType)
    nansatObjIceChart = add_colortable(nansatObjIceChart, cfg.sourceType)
    nansatObjIceChart.export(ofile, bands=[1], driver='GTiff')
    if cfg.quicklook:
        rgb = np.zeros((classID.shape[0], classID.shape[1], 3), 'uint8')
        for k in colorDict[cfg.sourceType].keys():
            rgb[classID==k,:] = colorDict[cfg.sourceType][k]
        plt.imsave(ofile.replace('.tif', '.png'), rgb)

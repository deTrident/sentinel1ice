import os
from nansat import *
import scipy.stats as st
from django.contrib.gis.geos import Polygon
from multiprocessing import Pool


def mean_sigma0(eaMinMax):
    ''' Compute mean and std of sigma0 for given range of EA'''
    print eaMinMax[0]
    gpi = (ea >= eaMinMax[1]) * (ea < eaMinMax[2]) * finiteS0
    sigma0_HVgpi = sigma0_HV[gpi]
    return np.mean((eaMinMax[1], eaMinMax[2])), np.std(sigma0_HVgpi), np.mean(sigma0_HVgpi)


import os, sys
print sys.path.append('/home/vagrant/py/nansen-cloud/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nansencloud.settings")
import django
django.setup()

from cat.models import Image

p = Polygon(((-10, 60), (26, 60), (26, 74), (-10, 74), (-10, 60)))
images = Image.objects.filter(border__intersects=p).filter(sourcefile__name__startswith='S1A_EW_GRDM_1SDH')
print len(images)

for img in images[::10]:
    ofile = img.sourcefile.name + '.npz'
    s0file = ofile + 's0.npz'

    if os.path.exists(ofile):
        print '%s already exists' % ofile
        continue

    print img.sourcefile.name

    # load data from original file
    n = img.get_nansat()
    wm = n.watermask('/files/MOD44W/')

    # get elevation angle
    ea = n['elevation_angle']

    # get sigma0 HV
    sigma0_HV = n['sigma0_HV']
    del n
    sigma0_HV[sigma0_HV == 0] = np.nan
    # convert to DB
    sigma0_HV = 10 * np.log10(sigma0_HV)

    # blank watermask
    print 'Get watermask'
    wm = wm[1]
    sigma0_HV[wm == 2] = np.nan
    del wm

        # save for later
        #np.savez_compressed(s0file, ea=ea, sigma0_HV=sigma0_HV)

    # get elevation-angle-wise mean, median and STD
    # 1. get mean EA (single row)
    eaMean = np.mean(ea, axis=0)

    # get stats not for each EA
    eaMean = eaMean[::3]

    # 2. for each EA sample find corresponding sigma0HV
    #     and calculate mean, median, std
    print 'Compute stats for %d EA values ' % len(eaMean)
    finiteS0 = np.isfinite(sigma0_HV)

    eaMinMax = zip(range(len(eaMean[:-1])), eaMean[:-1], eaMean[1:])

    p = Pool(5)
    sigma0_HV_stats = np.array(p.map(mean_sigma0, eaMinMax))

    del sigma0_HV
    del ea
    del finiteS0

    # save all data
    np.savez_compressed(ofile, sigma0_HV_stats=sigma0_HV_stats)
    print 'OK'
    del sigma0_HV_stats
    del eaMinMax
    

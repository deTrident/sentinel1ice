import os
from nansat import *
import scipy.stats as st
from django.contrib.gis.geos import Polygon
from multiprocessing import Pool


import os, sys
print sys.path.append('/home/vagrant/py/nansen-cloud/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nansencloud.settings")
import django
django.setup()

from cat.models import Image

def extract_mean_HH(img):
    ofile = img.sourcefile.name + '_HH_stats.npz'

    if os.path.exists(ofile):
        print '%s already exists' % ofile
        return

    print img.sourcefile.name

    # load data from original file
    n = img.get_nansat()
    print 'Open - OK'
    n.resize(0.1)
    wm = n.watermask('/files/MOD44W/')

    # get elevation angle
    ea = n['elevation_angle']

    # get sigma0 HH
    sigma0_HH = n['sigma0_HH']
    sigma0_HH[sigma0_HH == 0] = np.nan
    # convert to DB
    sigma0_HH = 10 * np.log10(sigma0_HH)

    # blank watermask
    print 'Get watermask'
    wm = wm[1]
    sigma0_HH[wm == 2] = np.nan
    del wm

    # get elevation-angle-wise mean, median and STD
    # 1. get mean EA (single row)
    eaMean = np.mean(ea, axis=0)

    s0HHStd    = np.nanstd(sigma0_HH, axis=0)
    s0HHMean   = np.nanmean(sigma0_HH, axis=0)

    del sigma0_HH
    del ea

    # save all data
    np.savez_compressed(ofile, sigma0_HH_stats=[eaMean, s0HHStd, s0HHMean])
    print 'OK'



p = Polygon(((20, 83), (21, 83), (21, 84), (20, 84), (20, 83)))
images = Image.objects.filter(border__intersects=p).filter(sourcefile__name__startswith='S1A_EW_GRDM_1SDH')
print len(images)

pool = Pool(4)
pool.map(extract_mean_HH, images[::4])    

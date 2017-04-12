''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob, zipfile, shutil
import numpy as np
from sentinel1denoised.S1_EW_GRD_NoiseCorrection import Sentinel1Image
from sar2ice import export_uint8_jpeg
from config import get_env


# find input files
idir = get_env()['inputDirectory']
odir = get_env()['outputDirectory']
ifiles = sorted(glob.glob(idir+'S1[AB]_EW_GRDM_1SDH_*.zip'),reverse=False)
'''
minDate,maxDate = '20151220','20160331'
ifiles = [ ifile for ifile in ifiles
           if minDate <= os.path.split(ifile)[-1][17:25] <= maxDate ]
'''
for ifile in ifiles:
    
    ifilename = os.path.split(ifile)[1]
    ID = ifilename.split('.')[0]
    if not os.path.exists(odir+ID):
        os.mkdir(odir+ID)
    ofile = { 'HH': os.path.join(odir+ID,ID+'_HH_sigma0.npz'),
              'HV': os.path.join(odir+ID,ID+'_HV_sigma0.npz')  }
    if os.path.exists(ofile['HH']) and os.path.exists(ofile['HV']):
        continue
    else:
        with zipfile.ZipFile(ifile, "r") as z:
            z.extractall()
    ifilename = ifilename[:-3]+'SAFE'

    for pol in ['HH','HV']:
        
        if os.path.exists(ofile[pol]):
            continue
        results = {}
        print 'Run denoising of sigma0_%s in %s' % (pol, ifilename)
        s1i = Sentinel1Image(ifilename)
        ### CAUTION: gap filling should be avoided. it distorts image statistics.
        s1i.add_denoised_band( 'sigma0_%s' % pol,
            denoAlg='NERSC', addPow='EW0', clipDirtyPx=True, adaptNoiSc=False,
            angDepCor=True, fillVoid=False, dBconv=False, development=True )

        # multi-look
        multiLookFactor = get_env()['multiLookFactor']
        skipGCPs = 4          # choose from [1,2,4,5]
        if multiLookFactor!=1:
            skipGCPs = np.ceil(skipGCPs/float(multiLookFactor))
            s1i.resize(factor=1./multiLookFactor)

        results['sigma0'] = 10*np.log10(s1i['sigma0_%s_denoised' % pol])
        results['inc_ang'] = np.nanmean(s1i['incidence_angle'],axis=0)
        results['ssw'] = s1i['subswath_indices']
        sigma0raw = 10*np.log10(s1i['sigma0_%s_raw' % pol])

        # generate watermask
        nGCPs = s1i.vrt.dataset.GetGCPCount()
        GCPs = s1i.vrt.dataset.GetGCPs()
        idx = np.arange(0,nGCPs).reshape(nGCPs//21,21)
        skipGCPsRow = max( [ y for y in range(1,nGCPs//21)
                         if ((nGCPs//21 -1) % y == 0) and y <= skipGCPs ] )
        smpGCPs = [ GCPs[i] for i in np.concatenate(idx[::skipGCPsRow,::skipGCPs]) ]
        GCPProj = s1i.vrt.dataset.GetGCPProjection()
        dummy = s1i.vrt.dataset.SetGCPs(smpGCPs,GCPProj)
        results['wm'] = s1i.watermask(tps=True)[1]
        dummy = s1i.vrt.dataset.SetGCPs(GCPs,GCPProj)

        # compute histograms
        bin_edges = np.arange(-40.25,+10.75,0.5)
        results['raw_hist'] = np.histogram(
            sigma0raw[ np.isfinite(sigma0raw) * (results['wm']!=2) ],
            bins=bin_edges )
        results['denoised_hist'] = np.histogram(
            results['sigma0'][ np.isfinite(results['sigma0'])*(results['wm']!=2) ],
            bins=bin_edges )

        # create quickview
        print 'Make full resolution JPG'
        vmin, vmax = np.percentile(
            results['sigma0'][ np.isfinite(results['sigma0'])
                               * (results['wm']!=2) ], (1.,99.) )
        '''
        plt.imsave( ofile[pol].replace('.npz','_original.jpg'), sigma0raw,
                    vmin=vmin, vmax=vmax, cmap='gray')
        plt.imsave( ofile[pol].replace('.npz','_denoised.jpg'), results['sigma0'],
                    vmin=vmin, vmax=vmax, cmap='gray')
        '''
        export_uint8_jpeg( ofile[pol].replace('.npz','_original.jpg'),
                                sigma0raw, vmin=vmin, vmax=vmax )
        export_uint8_jpeg( ofile[pol].replace('.npz','_denoised.jpg'),
                                results['sigma0'], vmin=vmin, vmax=vmax )

        # save denoised data
        np.savez_compressed(ofile[pol] , **results)
        del s1i

    if os.path.exists(ifilename):
        shutil.rmtree(ifilename)

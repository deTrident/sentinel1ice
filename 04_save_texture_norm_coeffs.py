import os, glob
import numpy as np
import matplotlib.pyplot as plt
from sar2ice import compute_transform_coeffs

"""
Join Haralick texture features from many files
Transform some of them
Center on mean and normalize by STD
Save normalized per input file
"""
trans_thres = 0.
trans_alg = 'boxcox'
percentile = 0.1
idir = ( os.path.abspath(os.getcwd()+'/../shared/test_data/sentinel1a_l1')
         + '/odata_FramStrait_TFs/' )
normFilePrefix = 'norm01'

# find normalization coeeficients independently for HH and HV
print('Compute coefficients for texture feature normalization.')
print('POL  TF#  TRANSFORM    oSKEW    oMIN    oMAX     nSKEW    nMIN    nMAX')

for pol in ['HH', 'HV']:
    
    normFile = os.path.join(idir, normFilePrefix + pol + '.npy')
    ifiles = sorted(glob.glob(idir + '*%s_har.npz' % pol))
    # read TFs from many input images and keep in joinedTF
    joinedTF = []
    for ifile in ifiles:
        harData = np.load(ifile)['tfs']
        joinedTF.append(harData.reshape(13, harData.shape[1]*harData.shape[2]))
    joinedTF = np.hstack(joinedTF)

    # data transform TF if needed. center and normalize
    # keep transform parameters of each TF
    tfStds = []
    tfMeans = []
    tfSkews = []
    transPar1 = []
    transPar2 = []
    for i, tf in enumerate(joinedTF):
        
        print(' %s   %02d ' %(pol,i)),
        newTF, statVec, newTFSkew = compute_transform_coeffs(
            tf, percentile=percentile, algorithm=trans_alg, skew_thres=trans_thres )
        tfSkews.append(statVec[0])
        transPar1.append(statVec[1])
        transPar2.append(statVec[2])
        tfMeans.append(statVec[3])
        tfStds.append(statVec[4])
        
        tfSkew = statVec[0]
        oldTFMin, oldTFMax = np.percentile(
            tf[np.isfinite(tf)], (percentile, 100-percentile) )
        newTFMin, newTFMax = np.percentile(
            newTF[np.isfinite(newTF)], (percentile, 100-percentile) )
        print('  %+.3f  %+.3f  %+.3f    %+.3f  %+.3f  %+.3f'
              %(tfSkew, oldTFMin, oldTFMax, newTFSkew, newTFMin, newTFMax))
        hist_bins = np.linspace(min(oldTFMin,newTFMin),max(oldTFMax,newTFMax),101)
        oldHist = np.histogram(tf[np.isfinite(tf)],hist_bins)
        newHist = np.histogram(newTF[np.isfinite(newTF)],hist_bins)
        
        plt.plot(hist_bins[:-1]+np.diff(hist_bins)/2,oldHist[0])
        plt.plot(hist_bins[:-1]+np.diff(hist_bins)/2,newHist[0])
        plt.title('%s %02d %+.3f %+.3f %+.3f %+.3f %+.3f %+.3f'
            % (pol, i, tfSkew, oldTFMin, oldTFMax, newTFSkew, newTFMin, newTFMax))
        plt.savefig(idir + 'tf_norm_hist%s_%02d.png' % (pol, i),
                    dpi=150, bbox_inches='tight', pad_inches=0)
        plt.close('all')

    # save log, mean and std to use in operational processing
    normCoefs = np.vstack([tfSkews, transPar1, transPar2, tfMeans, tfStds])
    np.save(normFile, normCoefs)

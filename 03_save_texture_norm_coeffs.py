''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from sar2ice import compute_transform_coeffs
from scipy.stats import skew
from config import get_env


trans_alg = get_env()['textureFeatureNormalization']
idir = get_env()['outputDirectory']
normFilePrefix = get_env()['textureFeatureNormalizationFilePrefix']

# find normalization coeeficients independently for HH and HV
print('Compute coefficients for texture feature normalization.')
print('POL  TF#  TRANSFORM    oSKEW    oMIN    oMAX     nSKEW    nMIN    nMAX')

for pol in ['HH', 'HV']:
    
    normFile = normFilePrefix+pol+'.npz'
    ifiles = sorted(glob.glob(idir+'*/*%s_har.npz' % pol))
    # read TFs from many input images and keep in joinedTF
    joinedTF = []
    for ifile in ifiles:
        harData = np.load(ifile)['tfs']
        joinedTF.append(harData.reshape(13, harData.shape[1]*harData.shape[2]))
    joinedTF = np.hstack(joinedTF)

    # data transform TF if needed. center and normalize
    # keep transform parameters of each TF
    ignore_saturated = [ 1, 0, 1, 0, 1, 0, 0, 0, 0, np.nanmax(joinedTF[9]), 0, 0, 0 ]
    normCoeffs = np.zeros((13,5))
    for i,TF in enumerate(joinedTF):
        
        print(' %s   %02d ' %(pol,i)),
        TF = TF[np.isfinite(TF)*(TF!=ignore_saturated[i])]
        newTF,normCoeffs[i,:] = compute_transform_coeffs(TF,algorithm=trans_alg)
        oldTFMin,oldTFMax = np.min(TF), np.max(TF)
        newTFMin,newTFMax = np.min(newTF), np.max(newTF)
        TFskew,newTFskew = skew(TF),skew(newTF)
        print('  %+.3f  %+.3f  %+.3f    %+.3f  %+.3f  %+.3f'
              %(TFskew, oldTFMin, oldTFMax, newTFskew, newTFMin, newTFMax))
        hist_bins = np.linspace(min(oldTFMin,newTFMin),max(oldTFMax,newTFMax),1000)
        oldHist = np.histogram(TF,hist_bins)
        newHist = np.histogram(newTF,hist_bins)

        plt.plot(hist_bins[:-1]+np.diff(hist_bins)/2,oldHist[0])
        plt.plot(hist_bins[:-1]+np.diff(hist_bins)/2,newHist[0])
        plt.title('%s %02d %+.3f %+.3f %+.3f %+.3f %+.3f %+.3f'
            % (pol, i, TFskew, oldTFMin, oldTFMax, newTFskew, newTFMin, newTFMax))
        plt.savefig(idir + 'tf_norm_hist%s_%02d.png' % (pol, i),
                    dpi=150, bbox_inches='tight', pad_inches=0)
        plt.close('all')

    # save log, mean and std to use in operational processing
    np.savez(normFile, normAlg=trans_alg ,normCoeffs=normCoeffs)

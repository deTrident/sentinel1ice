''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
from config import get_env

idir = get_env()['outputDirectory']

low_edge = 0.1  # threshold for clipping extreme values
high_edge = 0.1  # threshold for clipping extreme values

# find input files
ifiles = sorted(glob.glob(idir + '*/S1?_EW_GRDM_1SDH*_gamma0.npz'))


for pol in ['HH','HV']:

    # compute effective dynamic range for texture analysis
    hist_bin_edges = np.load(ifiles[0])['denoised_gamma0_%s_hist' % pol][1]
    hist_stack = np.zeros(hist_bin_edges.size-1)
    for ifile in ifiles:
        hist_stack = np.vstack([hist_stack, np.load(ifile)['denoised_gamma0_%s_hist' % pol][0]])
    hist_stack = hist_stack[1:]
    hist_sum = np.sum(hist_stack)
    hist_cum = np.cumsum(np.sum(hist_stack,axis=0))
    gamma0_min = hist_bin_edges[np.where(hist_cum < low_edge/100. * hist_sum)[0][-1]+1]
    gamma0_max = hist_bin_edges[np.where(hist_cum > (100-high_edge)/100. * hist_sum)[0][0]]
    print( '%s gamma0 range (%3.1f-%3.1f%%): %.2f dB to %.2f dB'
           % (pol,low_edge,100-high_edge,gamma0_min,gamma0_max))
    plt.plot( hist_bin_edges[:-1]+np.diff(hist_bin_edges)/2, np.sum(hist_stack,axis=0), label='%s' %pol )

plt.xlabel('Gamma nought (dB)'), plt.ylabel('Number of samples')
plt.title(r'$\gamma^0$' + ' distributions from %d land-masked images' % len(ifiles))
plt.legend()
plt.tight_layout()
plt.savefig('gamma0_distribution.png')

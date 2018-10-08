''' Use built-in backend AGG to prevent X server error.
    This error happens when work in remote server through ssh '''
import matplotlib;    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, glob
import numpy as np
import config as cfg

low_edge = {'HH':0.1, 'HV':0.1}  # threshold for clipping extreme values
high_edge = {'HH':0.1, 'HV':0.1}  # threshold for clipping extreme values

# find input files
ifiles = sorted(glob.glob(cfg.outputDirectory + '*/S1?_EW_GRDM_1SDH*_sigma0.npz'))


for pol in ['HH','HV']:
    for dtype in ['raw','denoised']:
        key = pol + '_' + dtype
        # compute effective dynamic range for texture analysis
        hist_bin_edges = np.load(ifiles[0])['sigma0_%s_hist' % key][1]
        hist_stack = np.zeros(hist_bin_edges.size-1)
        for ifile in ifiles:
            hist_stack = np.vstack([hist_stack, np.load(ifile)['sigma0_%s_hist' % key][0]])
        hist_stack = hist_stack[1:]
        hist_sum = np.sum(hist_stack)
        hist_cum = np.cumsum(np.sum(hist_stack,axis=0))
        sigma0_min = hist_bin_edges[np.where(hist_cum < low_edge[pol]/100. * hist_sum)[0][-1]+1]
        sigma0_max = hist_bin_edges[np.where(hist_cum > (100-high_edge[pol])/100. * hist_sum)[0][0]]
        print( '%s sigma0 range (%3.2f-%3.2f%%): %.2f dB to %.2f dB'
              % (key,low_edge[pol],100-high_edge[pol],sigma0_min,sigma0_max))
        plt.plot( hist_bin_edges[:-1]+np.diff(hist_bin_edges)/2, np.sum(hist_stack,axis=0), label='%s' % key )

plt.xlabel('Sigma nought (dB)'), plt.ylabel('Number of samples')
plt.title(r'$\sigma^0$' + ' distributions from %d images' % len(ifiles))
plt.legend()
plt.tight_layout()
plt.savefig('sigma0_distribution.png', dpi=300)

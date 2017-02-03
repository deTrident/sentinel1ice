import os, glob
import numpy as np
import matplotlib.pyplot as plt

idir = '/Volumes/ExFAT2TB/Sentinel1A/odata_FramStrait_denoised/'

edge_percent = 0.5  # threshold for clipping extreme values

for pol in ['HH','HV']:

    # find input files
    ifiles = sorted(glob.glob(idir + 'S1A_EW_GRDM_1SDH*%s_s0.npz' % pol),reverse=False)

    # compute effective dynamic range for texture analysis
    hist_bin_edges = np.load(ifiles[0])['denoised_hist'][1]
    hist_stack = np.zeros(hist_bin_edges.size-1)
    for ifile in ifiles:
        hist_stack = np.vstack([hist_stack, np.load(ifile)['denoised_hist'][0]])
    hist_stack = hist_stack[1:]
    hist_sum = np.sum(hist_stack)
    hist_cum = np.cumsum(np.sum(hist_stack,axis=0))
    sigma0_min = hist_bin_edges[np.where(hist_cum < edge_percent/100 * hist_sum)[0][-1]+1]
    sigma0_max = hist_bin_edges[np.where(hist_cum > (100-edge_percent)/100 * hist_sum)[0][0]]
    print( '%s sigma0 range (%3.1f-%3.1f%%): %.2f dB to %.2f dB'
           % (pol,edge_percent,100-edge_percent,sigma0_min,sigma0_max))
    plt.plot( hist_bin_edges[:-1]+np.diff(hist_bin_edges)/2, np.sum(hist_stack,axis=0), label='%s' %pol )

plt.xlabel('sigma0'), plt.ylabel('frequency')
plt.title('sigma0 distributions extracted from %d images' % len(ifiles))
plt.legend()
plt.savefig('sigma0_distribution.png')

import os
import sys
sys.path.append('/home/vagrant/py/')
from radarsat2ice import *
from nansat import *
from zoning import *

filename = 'S1A_EW_GRDM_1SDH_20150207T151223_20150207T151323_004519_0058C6_9A73.SAFE'
sigma0bands = {}
for bandName in ['sigma0_HH', 'sigma0_HV']:
    s0Name = filename + bandName + '.npy'
    print s0Name

    if os.path.exists(s0Name):
        sigma0 = np.load(s0Name)
        cmin, cmax = sigma0.min(), sigma0.max()
    else:
        n = Nansat(filename)
        sigma0 = 10 * np.log10(n[bandName][6000:, ])

        # save JPG figure
        f = Figure(sigma0)
        cmin, cmax = f.clim_from_histogram(ratio=0.99)
        f.process(cmin=cmin, cmax=cmax, cmapName='gray')
        f.save(s0Name + '.jpg')

        # clip and save data
        sigma0[sigma0 < cmin] = cmin
        sigma0[sigma0 > cmax] = cmax
        np.save(s0Name, sigma0)


    sigma0bands[bandName] = sigma0
    print sigma0.shape, cmin, cmax
raise
stp = 32

for d in [2]:#4, 8, 16]:
    for l in [8]:#16, 32, 64]:
        for s in [16]:#32, 64, 128]:
            print '\n\nExp: d %d l %d s %d\n\n' % (d, l, s)
            tfs = []
            for bandName in ['sigma0_HH', 'sigma0_HV']:
                sigma0 = sigma0bands[bandName][:, :2900]
                cmin, cmax = sigma0.min(), sigma0.max()
                glcm_nn = GLCM_NN(l=l, stp=stp, d=d, s=s, threads=4)
                tf = glcm_nn.compute_textures(sigma0, clim=[cmin, cmax])
                pcs = pca(tf, 6, oPrefix=bandName+'_d%02d_l%02d_s%03d_' % (d, l, s))
                tfs.append(tf)

            tfs = np.vstack(tfs)

            pcs = pca(tfs, 6, oPrefix='comb_d%02d_l%02d_s%03d_' % (d, l, s))

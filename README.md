# sentinel1ice
Ice/water classification of Sentinel1 SAR data

* extract_hv_stats.py - for multiple scenes: save statistics of average dependence of sigma0_HV on elevation angle;
* extract_hh_stats.py - for multiple scenes: save statistics of average dependence of sigma0_HH on elevation angle;
* save_averaged_noise.py - average statistics of sigma0 dependece on EA from many scenes and save as thermal noise;
* remove_noise.py - remove thermal noise (and angular dependence) several scenes;
* test_text_feat_options.py - test influence of TF calculation options on results of cluster analysis;

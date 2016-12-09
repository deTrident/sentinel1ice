# sentinel1ice
## Ice/water classification of Sentinel1 SAR data
 * 00_segmentation.py - preprocess for segmentation based classification.
 * 01_denoise_sigma0.py - apply thermal noise correction.
 * 02_denoise_subwindow_stat.py - apply subwindow-wise special noise correction.
 * 03_calculate_text_features.py - calculate texture features.
 * 04_save_texture_norm_coefs.py - find and save texture feature normalization coefficients
 * 05_normalize_texture_features.py - normalize texture features
 * 06_pca_based_segmentation.py - run PCA and K-means classification. Save PCA and ZONES maps
 * 07_train_svm.py - after manual reclassification train SVM
 * 08_apply_svm.py - apply the trained SVM

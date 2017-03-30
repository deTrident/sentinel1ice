# sentinel1ice
## Ice/water classification of Sentinel1 SAR data
 * 00_segmentation.py - preprocess for segmentation based classification.
 * 01_denoise_sigma0.py - apply thermal noise correction.
 * 02_calculate_text_features.py - calculate texture features.
 * 03_save_texture_norm_coefs.py - find and save texture feature normalization coefficients
 * 04_normalize_texture_features.py - normalize texture features
 * 05_pca_based_segmentation.py - run PCA and K-means classification. Save PCA and ZONES maps
 * 06_train_svm.py - after manual reclassification train SVM
 * 07_apply_svm.py - apply the trained SVM

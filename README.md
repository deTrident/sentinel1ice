# sentinel1ice
## Ice/water classification of Sentinel1 SAR data

 * 01calculate_text_features.py - apply thermal noise correction from [sentinel1denoised](https://github.com/nansencenter/sentinel1denoised) and calculate texture features using [mahotas](https://pypi.python.org/pypi/mahotas)
 * 02save_norm_coefs.py - find and save (log-)normalization coefficients
 * 03normalize_tf.py - (log-)normalize texture features
 * 04run_pca.py - run PCA and K-means classification. Save PCA and ZONES maps
 * 05train_svm.py - after manual reclassification train SVM
 * 06apply_svm.py - apply the trained SVM

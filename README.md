# sentinel1ice
## Ice/water classification of Sentinel1 SAR data
 * 01_denoise_images.py - apply thermal noise correction, land masking and gray scale conversion.
 * 01_denoise_images_pp.py - parallel processing of 01_denoise_images.py
 * 02_calculate_text_features.py - calculate texture features.
 * 03a_rasterize_ice_chart.py - rasterize vector formatted ice chart into rasterized SAR image geometry.
 * 03b_segmentation.py - make segmentation image to help manual classification.
 * 04a_train_classifier_svm.py - train support vector machine based classifier.
 * 04b_train_classifier_rf.py - train random forest based classifier.
 * 05_apply_svm.py - apply classifier to the texture features.

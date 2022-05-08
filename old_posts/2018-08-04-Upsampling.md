---
layout: post 
title: Data Upsampling Notes 
date: 2018-08-04 16:20:23 +0900 
category: ML 
tag: deeplearning
---


* To combat the issue of imbalanced class sizes, upsample/oversample the minority class or undersample the majority class using resampling (bootstrapping) techniques could be used.
* In image classification, synthetic/augmented data could be used. The solution for imbalanced text corpora is less clear.
* Markov Chains do well to string together words that would logically follow one another, regardless of whether the sentences are are grammatically/syntactically sound or not, this idea could be used for text upsampling.
* Available other methods: Random Over Sampling, Smote(Synthetic Minority Oversampling Technique), BorderLine Smote, KMeans Smote, SVM Smote, ADASYN(Adaptive Synthetic Sampling), Smote-NC((Nominal and Continuous, for a dataset with categorical features)).
* Random oversampling is the simplest oversampling technique to balance the imbalanced nature of the dataset. It balances the data by replicating the minority class samples. This does not cause any loss of information, but the dataset is prone to overfitting as the same information is copied.
* In the case of random oversampling, it was prone to overfitting as the minority class samples are replicated, here SMOTE comes into the picture. SMOTE stands for Synthetic Minority Oversampling Technique. It creates new synthetic samples to balance the dataset.
SMOTE works by utilizing a k-nearest neighbor algorithm to create synthetic data. 
* Due to the presence of some minority points or outliers within the region of majority class points, bridges of minority class points are created. This is a problem in the case of Smote and is solved using Borderline Smote.
* K-Means SMOTE is an oversampling method for class-imbalanced data. It aids classification by generating minority class samples in safe and crucial areas of the input space. The method avoids the generation of noise and effectively overcomes imbalances between and within classes.
* Another variation of Borderline-SMOTE is Borderline-SMOTE SVM, or we could just call it SVM-SMOTE. This technique incorporates the SVM algorithm to identify the misclassification points.
* Borderline Smote gives more importance or creates synthetic points using only the extreme observations that are the border points and ignores the rest of minority class points. This problem is solved by the ADASYN algorithm, as it creates synthetic data according to the data density.
* Smote oversampling technique only works for the dataset with all continuous features. For a dataset with categorical features, we have a variation of Smote, which is Smote-NC (Nominal and Continuous).
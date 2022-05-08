---
layout: post 
title: Fairseq Multilingual Translation
date: 2020-11-03 16:20:23 +0900 
category: NLP
tag: deeplearning
---
Key developments:
1. Many-to-Many multilingual translation model(non-English-Centric models) that can translate directly between any pair of 100 languages. 
2. Covers thousands of language directions in training data.
3. Transformer-based neural machine translation models.

    <p align="center"> <img width="800" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/5.png?raw=true"> </p>
    <center>Fig 1: Translating from Chinese to French with Dense + Language-Specific Sparse Model </center>


4. Controls the distribution of word tokens for different languages found using [SentencePiece](https://web.archive.org/web/20210126045439/https://github.com/google/sentencepiece) from multilingual dataset.
5. A special token in the encoder indicating the source language and a
special token in the decoder indicating the target language were added.
6. Evaluated the quality of translations with [BLEU](https://web.archive.org/web/20210125155630/http://en.wikipedia.org/wiki/BLEU) and Human evaluation.
7.  Built parallel corpus of multilingual translation text using [LASER](https://web.archive.org/web/20201130004845/https://github.com/facebookresearch/LASER) embeddings, FAISS indexing(checking semantic similarity) and from mided data from [CCMatrix](https://web.archive.org/web/20201121182319/https://github.com/facebookresearch/LASER/tree/master/tasks/CCMatrix), CCAligned projects. 
8. Bitext data were mined based on language families and bridge languages.

    <p align="center">
  <img width="600" height="290" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/6.png?raw=true">
    </p>

9. Languages were grouped by linguistic similarity, geographic and cultural proximity.
   
10. Selective augmenting Bitext Data with Backtranslation 
11. Added Language-Specific layers to Pre-Trained Transformers(at the
end of the decoder) for improving performance.
    <p align="center"><img width="600" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/7.png?raw=true"></p>
    <center>Fig 3: Comparison on various evaluation settings </center>

    <p align="center"><img width="800" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/8.png?raw=true">
    </p>
    <center>Fig 4: Human Evaluation of Translation Accuracy of M2M-100 on Non-English Directions. </center>


#### More Study Resources:

1. Beyond English-Centric Multilingual Machine Translation,
  by Fan, Angela and Bhosale, Shruti and Schwenk, Holger and Ma, Zhiyi and El-Kishky, Ahmed and Goyal, Siddharth and Baines, Mandeep and Celebi, Onur and Wenzek, Guillaume and Chaudhary, Vishrav and Goyal, Naman and Birch, Tom and Liptchinsky, Vitaliy and Edunov, Sergey and Grave, Edouard and Auli, Michael and Joulin, Armand.
   
2. Ccmatrix: Mining billions of high-quality parallel sentences on the web by Schwenk, Holger and Wenzek, Guillaume and Edunov, Sergey and Grave, Edouard and Joulin, Armand.

3. A Massive Collection of Cross-Lingual Web-Document Pairs by El-Kishky, Ahmed and Chaudhary, Vishrav and Guzman, Francisco and Koehn, Philipp.

4. CCAligned: A Massive Collection of Cross-Lingual Web-Document Pairs by Ahmed El-Kishky, Vishrav Chaudhary, Francisco Guzman, Philipp Koehn
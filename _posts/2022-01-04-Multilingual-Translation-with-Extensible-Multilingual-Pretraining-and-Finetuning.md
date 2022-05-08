---
layout: post
title: Multilingual Translation with Extensible Multilingual Pretraining and Finetuning
date: 2022-01-04 16:20:23 +0900
category: NLP
tag: deeplearning
---
* Finetuning on bitext(bilingual finetuning) to translate from
one language to another does not leverage the full
capacity of the multilingual pretraining.

* Multilingual translation models can be created through multilingual fine tuning.starting from pretrained models incor- porates the benefits of large quantities of unla- beled monolingual data, which is particularly important for low resource languages where bitext is not available.

* Multi-lingual translation models with multilingual
pretraining (with monolingual data) followed
by multilingual finetuning (with parallel data).

### Core Concepts:
1. **mBART** is trained as a de-
noising autoencoder, training to predict the original
text
2. Random span masking and order permutation used for creating text variation while training.
3. Instead of training a model
from language i to language j, a model is trained
to translate N languages to N other languages.
4. trained with temperature upsampling, which upsamples lower resource pairs so that the high resource languages do not dominate the training data.

<p align="center">
<img title="" width="200" height="80" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/9.png?raw=true" alt="">
</p>

5. On average, all models have around 5.7 to 7 BLEU points improvement over bilingual baselines.

<p align="center">
<img title="" width="800" height="290" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/10.png?raw=true" alt="">
</p>


However, multilingual finetuning would mean that the same model capacity must model many directions rather than just one, which could decrease performance.

<p align="center">
<img title="" width="400" height="290" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/11.png?raw=true" alt="">

</p>

Ref:
1. [Multilingual Translation with Extensible Multilingual Pretraining and Finetuning](https://arxiv.org/abs/2008.00401)


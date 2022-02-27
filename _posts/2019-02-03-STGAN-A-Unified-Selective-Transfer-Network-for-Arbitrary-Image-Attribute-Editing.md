---
layout: post 
title: STGAN A Unified Selective Transfer Network for Arbitrary Image Attribute Editing 
date: 2019-02-03 16:20:23 +0900 
category: VISION-AI 
tag: deeplearning
---

1. This work selectively takes the difference between target and source attribute vectors as input. Selective transfer units(STU) are used with encoder-decoder to adaptively select and modify encoder feature for enhanced attribute editing.

<p align="center">
  <img title="STGAN" width="600" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/13.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

2. In terms of **selective**, STGAN is suggested to (i) only consider the attributes to be changed, and (ii) selectively concatenate encoder feature in editing attribute irrelevant regions with decoder feature. In terms of **transfer**, STGAN is expected to adaptively modify encoder feature to match the requirement of varying editing task, thereby providing a unified model for handling both local and global attributes.
3. Tried to resolve problem with Skip Connections in AttGAN
4. For arbitrary image attribute editing, instead of full target attribute vector, only the attributes to be changed is considered.

<p align="center">
  <img title="STGAN" width="95" height="30" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/14.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

5. STGAN Architecture:

<p align="center">
  <img title="STGAN" width="650" height="290" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/15.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

<br>

<p align="center">
  <img title="STGAN" width="650" height="200" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/16.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

6. Comparison: 

<p align="center">
  <img title="STGAN" width="300" height="180" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/17.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

7. 13 attributes, including Bald, Bangs, Black Hair, Blond Hair, Brown Hair, Bushy Eyebrows, Eyeglasses, Male, Mouth Slightly Open, Mustache, No Beard, Pale Skin and Young were investigated.
8. Example of testing single attribute:

<p align="center">
  <img title="STGAN" width="300" height="300" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/18.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

<br>

<p align="center">
  <img title="STGAN" width="300" height="300" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/19.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

<br>
<p align="center">
  <img title="STGAN" width="300" height="300" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/20.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

<br>
<p align="center">
  <img title="STGAN" width="300" height="300" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/21.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

<br>





 
#### Resources:

1. [Github STGAN](https://github.com/csmliu/STGAN)
2. [STGAN: A Unified Selective Transfer Network for Arbitrary Image Attribute Editing](https://arxiv.org/abs/1904.09709)
3. [AttGAN: Facial Attribute Editing by Only Changing What You Want](https://arxiv.org/pdf/1711.10678.pdf)
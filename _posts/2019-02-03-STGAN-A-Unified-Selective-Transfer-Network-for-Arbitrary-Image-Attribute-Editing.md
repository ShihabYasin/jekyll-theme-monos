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
  <img title="STGAN" width="600" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/15.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

<br>

<p align="center">
  <img title="STGAN" width="600" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/16.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

6. Comparison: 

<p align="center">
  <img title="STGAN" width="600" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/17.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>

7. 13 attributes, including Bald, Bangs, Black Hair, Blond Hair, Brown Hair, Bushy Eyebrows, Eyeglasses, Male, Mouth Slightly Open, Mustache, No Beard, Pale Skin and Young were investigated.









What causes human to perform extreme on-line translation tolerance is still to find.

Human high-level visual systems has extreme on-line translation tolerance, to perform same level of cognitive task its
necessary to determine how could on-line invariance be integrated within vision models e.g. CNN variants.

Using [GAP](https://paperswithcode.com/method/global-average-pooling#:~:text=Global%20Average%20Pooling%20is%20a,in%20the%20last%20mlpconv%20layer.)
in CNN, the receptive fields of the neurons at the final layer of the model cover 100% of the pixel space.


<p align="center">
  <img title="Comparison of accuracy scores Using GAP(5) & without GAP(others)" width="400" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/3.png?raw=true" alt="Comparison of accuracy scores Using GAP(5) & without GAP(others)">
</p>
<center>Fig 2: Comparison of accuracy scores Using GAP(5) & without GAP(others)</center>



Large receptive fields in human visual system give human to have a greater degree of visual translation tolerance.

<p align="center">
  <img title="Accuracy Using GAP over no-GAP" width="400" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/4.png?raw=true" alt="Accuracy Using GAP over no-GAP">
</p>
<center> Fig 3: Accuracy Using GAP over no-GAP</center>


### Notes:

[GAP](https://paperswithcode.com/method/global-average-pooling#:~:text=Global%20Average%20Pooling%20is%20a,in%20the%20last%20mlpconv%20layer.): Global Average Pooling is a pooling operation designed to replace fully connected layers in classical CNNs. The
idea is to generate one feature map for each corresponding category of the classification task in the last mlpconv
layer. Global average pooling sums out the spatial
information, thus it is more robust to spatial translations of the input.

<p align="center">
  <img title="Global Average Pooling" width="400" height="300" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/2.png?raw=true" alt="Global Average Pooling">
</p>
<center> Fig 4: Global Average Pooling</center>

 
#### More Study Resources:

1. The visual system supports online translation invariance for object identification by Bowers, J. Vankov, I. & Ludwig
   C. in Psychonomic Bulletin Review.
2. A quantifiable testing of global translation invariance in convolutional and capsule networks by Qi, W.
3. Extreme Translation Tolerance in Humans and Machines by Ryan Blything, Ivan Vankov, Casimir J. Ludwig ,​ Jeffrey S.
   Bowers in 2019 Conference on Cognitive Computational Neuroscience.
4. Early differential sensitivity of evoked-potentials to local and global shape during the perception of
   three-dimensional objects by Leek, E. C., Roberts, M. V., Oliver, Z. J., Cristino, F., & Pegna, A. in
   Neuropsychologia.
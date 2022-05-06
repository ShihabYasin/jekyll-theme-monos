---
layout: post 
title: Translation Invariance of DeepLearning VisionAI Models 
date: 2020-02-03 16:20:23 +0900 
category: VISION-AI 
tag: deeplearning
---

Human are very good at recognising novel objects at one retinal location to other varying 9 to 18 degree of freedom.

Current days CNN models support highly restricted on-line translation tolerance having a dependency over their trained
tolerance from training dataset.

<p align="center">
  <img title="Behavioral studies of translation tolerance" width="600" height="190" src="https://github.com/ShihabYasin/shihabyasin.github.io/blob/gh-pages/public/img/1.png?raw=true" alt="Behavioral studies of translation tolerance">
</p>
<center>Fig 1: Behavioral studies of translation tolerance</center>


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
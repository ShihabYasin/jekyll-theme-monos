---
layout: post
title: Wav2Vec2 Huggingface ASR Fine Tuning (Notes)
date: 2020-11-03 16:20:23 +0900
category: NLP
tag: deeplearning
---

### Some Important Points:

1. Simplify the text labels(shorten/part words reasonably). Remember, the simpler the text labels, the easier it is for
the model to learn to predict those labels.
2. Match Sampling rate with the tuning Model of Tokenizer (trained data and tuning data sampling should be same e.g.
16kHz)
3. Collect all punctuation and letters +  + change“ ” -> | (word_delimiter_token="|")+ "unknown" token "[UNK]"+
"padding" token“[PAD]”
4. About “Wav2Vec2FeatureExtractor” params
* ⇒ do_normalize: Whether the input should be zero-mean-unit-variance normalized or not. Usually, speech models
perform better when normalizing the input
* return_attention_mask: Whether the model should make use of an attention_mask for batched inference. In general,
XLS-R models checkpoints should always use the attention_mask.


<pre class="code" style="background-color: rgb(217,238,239,255);">
from transformers import Wav2Vec2FeatureExtractor
feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=True)

Preprocess Data: audio resampler given by hugging face

common_voice_train = common_voice_train.cast_column("audio", Audio(sampling_rate=16_000))
common_voice_test = common_voice_test.cast_column("audio", Audio(sampling_rate=16_000))
</pre>


5. After above code listen for some random audio for quality check .


6. About training agrs:
* group_by_length makes training more efficient by grouping training samples of similar input length into one batch.
This can significantly speed up training time by heavily reducing the overall number of useless padding tokens that are passed through the model
* learning_rate and weight_decay were heuristically tuned until fine-tuning has become stable. Note that those
parameters strongly depend on the Common Voice dataset and might be suboptimal for other speech datasets.

1. Input Length Limitation Resolution:
https://www.reddit.com/r/MachineLearning/comments/genjvb/d_why_is_the_maximum_input_sequence_length_of/
* In case a demo crashes with an "Out-of-memory" error due to long audio, you might want to uncomment the following
lines to filter all sequences that are longer than 5 seconds for training.


<pre class="code" style="background-color: rgb(217,238,239,255);">
max_input_length_in_sec = 5.0
common_voice_train = common_voice_train.filter(lambda x: x < max_input_length_in_sec * processor.feature

</pre>


8. N-gram KenLM Integration(with fine tuned model) :

There is a small problem that 🤗 Transformers will not be happy about later on. The 5-gram correctly includes a
"Unknown" or <unk>, as well as a begin-of-sentence,     ```< s >``` token, but no end-of-sentence, ```"< /s >" ``` token. This sadly has to be corrected currently after the
build.

We can simply add the end-of-sentence token by adding the line 0 ```</s>``` -0.11831701(say -0.11831701 is for ```<s>```)below the begin-of-sentence token and increasing the ngram 1 count by 1.

<pre class="code" style="background-color: rgb(217,238,239,255);">
with open ("5gram.arpa", "r") as read_file, open ("5gram_correct.arpa", "w") as write_file:
has_added_eos = False
for line in read_file:
if not has_added_eos and "ngram 1=" in line:
count = line.strip ().split ("=")[-1]
write_file.write (line.replace (f"{count}", f"{int (count) + 1}"))
elif not has_added_eos and "<s>" in line:
write_file.write (line)
write_file.write (line.replace ("<s>", "</s>"))
has_added_eos = True
else:
write_file.write (line)
</pre>

### References:

1. [SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition](https://web.archive.org/web/20211124160343/https://arxiv.org/pdf/1904.08779.pdf)
2. [UNSUPERVISED CROSS-LINGUAL REPRESENTATION LEARNING FOR SPEECH RECOGNITION](https://web.archive.org/web/20211101231430/https://arxiv.org/pdf/2006.13979.pdf)
3. [Sequence Modeling With CTC](https://web.archive.org/web/20211207021548/https://distill.pub/2017/ctc/)
4. [wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations](https://web.archive.org/web/20220105140507/https://arxiv.org/pdf/2006.11477.pdf)
5. [Fine-Tune Wav2Vec2 for English ASR with 🤗 Transformers](https://web.archive.org/web/20211220033856/https://huggingface.co/blog/fine-tune-wav2vec2-english)
6. [An Illustrated Tour of Wav2vec 2.0](https://web.archive.org/web/20211210152148/https://jonathanbgn.com/2021/09/30/illustrated-wav2vec-2.html)






[//]: # (Rough:)

[//]: # (fine-tune:)

[//]: # ()
[//]: # ()
[//]: # (1. https://huggingface.co/arijitx/wav2vec2-large-xlsr-bengali)

[//]: # ()
[//]: # (2. https://huggingface.co/tanmoyio/wav2vec2-large-xlsr-bengali4. )

[//]: # ()
[//]: # (Other Resources:)

[//]: # ()
[//]: # (4. &#40;Base&#41;Germnan FineTuning :https://huggingface.co/diego-fustes/wav2vec2-large-xlsr-gl)

[//]: # (5. 1. https://github.com/voidful/wav2vec2-xlsr-multilingual-56)

[//]: # ()
[//]: # ( )




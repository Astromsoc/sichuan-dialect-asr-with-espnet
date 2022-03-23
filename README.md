# 737hw3: Automatic Speech Recognition with ESPNet
For Assignment #3, End-to-End Automatic Speech Recognition in 11-737: Multilingual Natural Language Processing, S22 @ CMU.


Team Members: Siyu Chen @Astromsoc, Zhiruo Wang @zorazrw


## Experiment Overview

- Dataset: Sichuan Dialect, Daily Conversational Speech (open sourced version)

    _available at https://magichub.com/datasets/sichuan-dialect-scripted-speech-corpus-daily-use-sentence/_
    
    __Note__: We exclude one of the contributor speakers from this dataset due to his scarcely intelligible accent and a misleading talking nature -- we know this sort of utterance is also an integral subgroup for the ASR task to solve, but for a nascent system we are building with such a small corpus, we believe this act of removal helps to at least prompt the model to learn something basic about our target dialect.

    
- Recipe reference: espnet/egs2/commonvoice/asr1/

- Experiment Setups
  * `0-Baseline`: baseline: direct End-to-End ASR on Sichuan Dialect to transcriptions in Chinese characters
  * `1-withSSLR`: with Self-Supervised Language Representation: leveraging TERA under `s3prl`
  * `2-withPinyin`: with Hanyu Pinyin: generating transcriptions in Hanyu Pinyin (without tones)
  * `3-ftOnMandarin`: finetuning pretrained model on Mandarin ASR: train on larger Mandarin speech data with the same architecture and finetune on Sichuan Dialect


## Results

For Experiment 0, 1 and 3, since they all output sequences of Chinese characters, we measure with CER (Character Error Rate). For Experiment 2, since it outputs sequences of Hanyu Pinyin with white spaces as the separator in-between, we refere to WER (Word Error Rate) as the criterion for model performance.

| Setup | Metrics | Split - dev/test| Improvement |
| :--- | :--- | :--- | :--- |
| 0-Baseline w/ LM | CER | 77.2 / 76.0 |  --- |
| 0-Baseline w/o LM | CER | 76.2 / 75.9 |  --- |
| 1-withSSLR w/ LM | CER | 39.5 / 41.0 |  48.8 / 46.1 |
| 1-withSSLR w/o LM | CER | 32.0 / 33.4 |  58.0 / 56.0 |
| 2-withPinyin w/ LM | WER | 18.1 / 17.5 |  --- |
| 2-withPinyinw/o LM | WER | 13.9 / 13.8 |  --- |
| 3-ftOnMandarin w/ LM | CER | 60.2 / 59.5 |  22.0 / 21.7 |
| 3-ftOnMandarin w/o LM | CER | 48.4 / 47.5 |  36.5 / 37.4 |


## Funny Discoveries

Due to the page limit of our assignment report, we did not include a separate section exclusively for error analysis, but just several mentions in short sentences. Still, we found out something really interesting from the perspective of native Sichuan Dialect speakers that we hope to extend some discussion on.


### Front and Back Nasals

Standard Mandarin (or Putonghua) places a clear boundary between front nasals (whose Hanyu Pinyin ending with `"an", "in", "en", etc`) and back nasals (with an additional `"g"` in Hanyu Pinyin, respectively `"ang", "ing", "eng"` for the previous examples). 

However, Sichuan Dialect is way less rigorous for this differentiation, where except for clearly different pronunciations (`"an"` against `"ang"`, similarly to the phonological difference of vowels between `"Han"` and `"hunt"`). 

We found our model perplexed by this phonological confusion and output results like:

```
# 2-withPinyin-withoutLM-dev
id: (g0001-g0001_0063)
Scores: (#C #S #D #I) 16 1 0 0
REF:  nei di xu yao shen me tiao jian cai neng zai jiao tang ju XING hun li 
HYP:  nei di xu yao shen me tiao jian cai neng zai jiao tang ju XIN  hun li 
Eval:                                                           S         
```


### Cacuminal and Flat Consonants

Standard Mandarin clearly differentiates cacuminal consonants (`"zh", "ch", "sh", "r"`, pronounced like a retroflex) and flat consonants (`"z", "c", "s"`, pronounced with a flat tongue in a low place). Sichuan Dialect speakers tend to pronounce them both as flat ones, while for the special consonant of `r`, they have an additional "phoneme" that sounds like a "sounded sibilant", eg. the sound of `s` in `useless`). 

This is also what fooled our model:

```
# 2-withPinyin-withoutLM-dev
id: (g0007-g0007_0265)
Scores: (#C #S #D #I) 13 1 0 4
REF:  ** *** ** *** fu jin zui pian yi de chu ZU  fang duo shao qian mei you 
HYP:  HE BEI DA XUE fu jin zui pian yi de chu ZHU fang duo shao qian mei you 
Eval: I  I   I  I                             S                              
```

### Special Phonological Shifts

Other phonological changes also prevail within Sichuan Dialect speakers that does not have a one-for-all rule for all Hanyu Pinyin alike. It includes:

- Shifts of Vowels
	* `e` to `o`(not existing alone in Mandarin, but usually in dipthongs)

		eg. `ge1 ge` ("brother") --> `go2 go1`
		
		```
		id: (g0001-g0001_0217)
		Scores: (#C #S #D #I) 13 1 0 0
		REF:  ting guan yu chang E  de gu shi yong ying yu zen me shuo 
		HYP:  ting guan yu chang WO de gu shi yong ying yu zen me shuo 
		Eval:                    S                                     	
		```
	
		
- Shifts of Consonants
	* `w` to `'n` (slight velar vibration) specially in `wo`
	
		eg. `wo3` 	("I, me")		 --> `('n) o4` (with velar vibration)
		
		```
		id: (g0001-g0001_0217)
		Scores: (#C #S #D #I) 13 1 0 0
		REF:  ting guan yu chang E  de gu shi yong ying yu zen me shuo 
		HYP:  ting guan yu chang WO de gu shi yong ying yu zen me shuo 
		Eval:                    S                                     	
		```
		This is actually the same example we quoted for the 1st shift of vowel (`e` to `o`), because the confusion of `wo` and `e` comes from presumably the fact that they are both pronounced as `'n o` in Sichuan Dialect.
		
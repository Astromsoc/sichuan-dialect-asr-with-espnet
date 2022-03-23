# 737hw3: Automatic Speech Recognition with ESPNet
For Assignment #3, End-to-End Automatic Speech Recognition in 11-737: Multilingual Natural Language Processing, S22 @ CMU.


Team Members: Siyu Chen @Astromsoc, Zhiruo Wang@zorazrw


## Experiment Overview

- Dataset: Sichuan Dialect, Daily Conversational Speech (open sourced version)
    available at https://magichub.com/datasets/sichuan-dialect-scripted-speech-corpus-daily-use-sentence/.
- Recipe reference: espnet/egs2/commonvoice/asr1/
- Experiment Setups
  * (1) baseline: direct End-to-End ASR on Sichuan Dialect to transcriptions in Chinese characters
  * (2) with Self-Supervised Language Representation: leveraging TERA under `s3prl`
  * (3) with Hanyu Pinyin: generating transcriptions in Hanyu Pinyin (without tones)
  * (4) finetuning pretrained model on Mandarin ASR: train on larger Mandarin speech data with the same architecture and finetune on Sichuan Dialect
 

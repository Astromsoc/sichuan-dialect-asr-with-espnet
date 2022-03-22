## Stage 1: Pretrained on Mandarin
# original training & inference from stage 2 to 13
bash asr.sh --stage 2 --stop_stage 13 --nj 6 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc" --audio_format "flac" --lm_train_text "data/train_sc/text" --token_type bpe --nbpe 4200 --bpemode "unigram" --bpe_train_text "data/train_sc/text" --asr_config "conf/3_ftOnMandarin.yaml" --ngpu 1 --use_lm true --inference_nj 6 --gpu_inference true 

## Stage 2: Finetuned on Sichuan Dialect
bash asr.sh --stage 2 --stop_stage 13 --nj 6 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc" --audio_format "flac" --lm_train_text "data/train_sc/text" --token_type bpe --nbpe 4200 --bpemode "unigram" --bpe_train_text "data/train_sc/text" --asr_config "conf/3_ftOnMandarin.yaml" --ngpu 1 --use_lm true --inference_nj 6 --gpu_inference true --speed_perturb_factors "0.9 1.0 1.1" --pretrained_model "exp/asr_3_ftOnMandarin_raw_zh-CN_bpe4200/50epoch.pth"

## Stage 3: Inferring without Language Model
bash asr.sh --stage 12 --stop_stage 13 --nj 6 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc" --audio_format "flac" --lm_train_text "data/train_sc/text" --token_type bpe --nbpe 4200 --bpemode "unigram" --bpe_train_text "data/train_sc/text" --asr_config "conf/3_ftOnMandarin.yaml" --ngpu 1 --use_lm false --inference_nj 6 --gpu_inference true --speed_perturb_factors "0.9 1.0 1.1" --pretrained_model "exp/asr_3_ftOnMandarin_raw_zh-CN_bpe4200/50epoch.pth"

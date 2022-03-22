# original training & inference from stage 2 to 13
bash asr.sh --stage 2 --stop_stage 13 --nj 6 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc" --audio_format "flac" --lm_train_text "data/train_sc/text" --token_type bpe --nbpe 3000 --bpemode "unigram" --bpe_train_text "data/train_sc/text" --asr_config "conf/0_baseline.yaml" --ngpu 1 --use_lm true --inference_nj 6 --gpu_inference true --speed_perturb_factors "0.9 1.0 1.1"

# # additional inference without language model
# bash asr.sh --stage 12 --stop_stage 13 --nj 6 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc" --audio_format "flac" --lm_train_text "data/train_sc/text" --token_type bpe --nbpe 3000 --bpemode "unigram" --bpe_train_text "data/train_sc/text" --asr_config "conf/0_baseline.yaml" --ngpu 1 --use_lm false --inference_nj 6 --gpu_inference true --speed_perturb_factors "0.9 1.0 1.1"

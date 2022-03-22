# original training & inference from stage 2 to 13
bash asr.sh --stage 2 --stop_stage 13 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc"   --nbpe 3000 --asr_config "conf/1_withSSRL.yaml" --use_lm true --token_type bpe --inference_nj 10 --nj 10 --feats_normalize uttmvn --speed_perturb_factors "0.9 1.0 1.1"

# # additional inference without language model
bash asr.sh --stage 12 --stop_stage 13 --train_set "train_sc" --valid_set "dev_sc" --test_sets "dev_sc test_sc" --lang "sc"   --nbpe 3000 --asr_config "conf/1_withSSRL.yaml" --use_lm false --token_type bpe --inference_nj 10 --nj 10 --feats_normalize uttmvn --speed_perturb_factors "0.9 1.0 1.1" 

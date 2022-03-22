## ***--***--***--***--***--***--***--***--***--***--** ##
## remember to remove suffix for the final texts to use ##
## ***--***--***--***--***--***--***--***--***--***--** ##

import re
import os
import numpy as np
from pypinyin import lazy_pinyin, Style

## *** BASE FILES *** ##
## DO NOT CHANGE THEM ##
RECORDINGS_DIR = 'WAV'
FILE_PATH = 'UTTRANSINFO.txt'
SPK_TO_UTR_PATH = 'spk2utt'
UTR_TO_SPK_PATH = 'utt2spk'

## *** OUTPUT  FOLDERS *** ##
## ALSO DO NOT CHANGE THEM ##
OUT_ROOT = 'data'
TRAIN_FOLDER = os.path.join(OUT_ROOT, 'train_sc')
DEV_FOLDER = os.path.join(OUT_ROOT, 'dev_sc')
TEST_FOLDER = os.path.join(OUT_ROOT, 'test_sc')

## *** OUTPUT FILES *** ##
##  STILL NO CHANGE PLZ ##
TEXT_PATH = 'text'
SCP_PATH = 'wav.scp'

## *** DYNAMIC HYPERPARAMS *** ##
##  PLAY WITH THEM AS YOU WISH ##
SPLIT_ON_SPK = False
SKIP_ACCENT = True
USE_PINYIN = False
REMOVE_LIST = {'G1108'}
TRAIN_RATE = 0.8            # train + dev + test = 1, dev = test
## FOR REPLICATIONS ##
np.random.seed(11737)


## MAIN FUNCTION ##

if __name__ == '__main__':

    if not os.path.exists(OUT_ROOT):
        os.mkdir(OUT_ROOT)

    ## LOAD TRANSCRIPTS ##

    full_contents = [f.strip() for f in open(FILE_PATH, 'r')]
    spk2utr, utr2spk = dict(), dict()
    utr2channel = dict()
    utr2text0, utr2text1, utr2text2 = dict(), dict(), dict()
    utr2pinyin, utr2pinyinT = dict(), dict()

    for l in full_contents[1:]:
        parts = l.split('\t')
        channel, file_name, spk_id = parts[0], parts[1], parts[2]
        # remove the ones with the strongest accent
        if SKIP_ACCENT and spk_id in REMOVE_LIST:
            continue
        utr_id = file_name.split('.')[0]
        text = re.sub('[，。？！!：、\s＜＞《》·]*', '', parts[-1].strip())
        # text1: sichuan vocab
        text1 = re.sub('【.*】', '', text)
        text1 = re.sub('[“”]', '', text1)
        # text2: mandarin equivalent
        text2 = re.sub('“.*”', '', text)
        text2 = re.sub('[【】]', '', text2)
        # pinyin: un-toned Pinyin
        pinyin = ' '.join(lazy_pinyin(text1))
        # pinyinT: toned Pinyin
        pinyinT = ' '.join(lazy_pinyin(text1, style=Style.TONE3, neutral_tone_with_five=True))

        # # Print if verbose -- no flag offered, please uncomment these lines to
        # # check scripts with replacements of dialectal vocabulary
        # if text1 != text2:
        #     print(f"\n\n{spk_id} - {utr_id}\n"
        #           f"{text}\n"
        #           f"{text1}\n"
        #           f"{text2}\n"
        #           f"{pinyin}\n"
        #           f"{pinyinT}\n")

        if spk_id not in spk2utr:
            spk2utr[spk_id] = list()
        spk2utr[spk_id].append(utr_id)

        utr2spk[utr_id] = spk_id
        utr2text0[utr_id] = text
        utr2text1[utr_id] = text1
        utr2text2[utr_id] = text2
        utr2pinyin[utr_id] = pinyin
        utr2pinyinT[utr_id] = pinyinT


    ## OUTPUT RESULTS ##
    if SPLIT_ON_SPK:

        all_speakers = [uid for uid in os.listdir(RECORDINGS_DIR)
                         if os.path.isdir(os.path.joint(RECORDINGS_DIR, uid))]
        all_speakers = np.random.permutation(all_users)

        train_count = int(TRAIN_RATE * len(all_speakers)) + 1
        dev_count = (now_count - train_count) // 2
        test_count = now_count - train_count - dev_count

        train_sc_uids = all_users[:train_count]
        dev_sc_uids = all_users[train_count: train_count + dev_count]
        test_sc_uids = all_users[-dev_count:]

        uids = [train_sc_uids, dev_sc_uids, test_sc_uids]
        folders = [TRAIN_FOLDER, DEV_FOLDER, TEST_FOLDER]

        for i, uid_list in enumerate(uids):
            fd = folders[i]
            print(f"In {fd}: there is/are {uid_list}.")
            uid_list = set(uid_list)
            if not os.path.exists(fd):
                os.mkdir(fd)

            # write out the results
            with open(os.path.join(fd, SPK_TO_UTR_PATH), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (spk_id, utr_id))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, UTR_TO_SPK_PATH), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (utr_id, spk_id))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_annotated'), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (utr_id, utr2text0[utr_id]))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH) + '_direct', 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (utr_id, utr2text1[utr_id]))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_stdvocab'), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (utr_id, utr2text2[utr_id]))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_pinyin'), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (utr_id, utr2text2[utr_id]))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_pinyinWithTones'), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write('%s %s\n' % (utr_id, utr2text2[utr_id]))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            scp_format = '%s ffmpeg -i WAV/%s/%s.wav -f wav -ar 16000 -ab 16 -ac 1 - |\n'
            with open(os.path.join(fd, SCP_PATH), 'w') as fw:
                for spk_id in uid_list:
                    for utr_id in spk2utr[spk_id]:
                        fw.write(scp_format % (utr_id, spk_id, utr_id))
                if len(uid_list) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

    else:

        trains, devs, tests = list(), list(), list()
        for spk, utrs in spk2utr.items():
            now_count = len(utrs)

            # Choice: split for each speaker
            train_count = int(TRAIN_RATE * now_count) + 1
            dev_count = (now_count - train_count) // 2
            test_count = now_count - train_count - dev_count

            utrs = list(np.random.permutation(list(utrs)))
            trains = trains + utrs[: train_count]
            devs = devs + utrs[train_count: train_count + dev_count]
            tests = tests + utrs[-test_count:]

        # # Choice: split randomly on a full set
        # train_count = int(TRAIN_RATE * len(utr2spk)) + 1
        # dev_count = (len(utr2spk) - train_count) // 2
        # test_count = len(utr2spk) - train_count - dev_count
        #
        # all_utterances = np.random.permutation(list(utr2spk.keys()))
        # trains = all_utterances[:train_count]
        # devs = all_utterances[train_count: train_count + dev_count]
        # tests = all_utterances[-test_count:]
        #
        # assert len(trains) + len(devs) + len(tests) == len(utr2spk)

        utr_sets = [trains, devs, tests]
        folders = [TRAIN_FOLDER, DEV_FOLDER, TEST_FOLDER]

        print('\nThere are a total of %d utterances in this dataset.\n' % (len(utr2spk)))

        for i, utr_set in enumerate(utr_sets):

            fd = folders[i]
            print(f"In {fd}: there are {len(utr_set)} utterances.")
            utrs = sorted(list(set(utr_set)))
            if not os.path.exists(fd):
                os.mkdir(fd)

            # write out the results
            with open(os.path.join(fd, SPK_TO_UTR_PATH), 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr2spk[utr], utr))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, UTR_TO_SPK_PATH), 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr, utr2spk[utr]))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_annotated'), 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr, utr2text0[utr]))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH) + '_direct', 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr, utr2text1[utr]))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_stdvocab'), 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr, utr2text2[utr]))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_pinyin'), 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr, utr2pinyin[utr]))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            with open(os.path.join(fd, TEXT_PATH + '_pinyinWithTones'), 'w') as fw:
                for utr in utrs:
                    fw.write('%s %s\n' % (utr, utr2pinyinT[utr]))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

            scp_format = '%s ffmpeg -i WAV/%s/%s.wav -f wav -ar 16000 -ab 16 -ac 1 - |\n'
            with open(os.path.join(fd, SCP_PATH), 'w') as fw:
                for utr in utrs:
                    fw.write(scp_format % (utr, utr2spk[utr], utr))
                if len(utrs) == 0:
                    fw.write(f"You are seeing this because there's either a "
                             f"problem in your dataset or the script is run "
                             f"on empty inputs for demo.")

    print("\nFinished. Have fun!\n\n\n")

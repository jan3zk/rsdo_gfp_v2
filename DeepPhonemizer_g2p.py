import dp
import os
import argparse
from dp.utils.io import read_config, save_config
from dp.preprocess import preprocess
from dp.train import train
from dp.phonemizer import Phonemizer
import numpy as np
from Levenshtein import distance as lev


def training(model_path, train_dict):
  with open(train_dict, 'r', encoding='utf-8') as f:
    lines = f.readlines()

  lines = [l.replace('\n', '') for l in lines]
  splits = [l.split(' ', 1) for l in lines]
  splits = [[s[0],s[1].replace(' ','')] for s in splits]
  train_data = [('sl_SL', s[0], s[1]) for s in splits if len(s)==2]

  # Manually set the grapheme and phoneme definitions in config file to 
  # comply with outputs of the following two commands
  dct = [l.split(' ', 1) for l in lines]
  graphemes = sorted(set(''.join([s[0] for s in dct])))
  phonemes = sorted(set(' '.join([s[1] for s in dct]).split(' ')))
  print('Učni grafemi: %s'%graphemes)
  print('Učni fonemi: %s'%phonemes)

  orig_config_file = 'config.yaml'
  mod_config_file = os.path.join(model_path, 'config.yaml')
  config = read_config(orig_config_file)
  config['paths']['checkpoint_dir'] = os.path.join(model_path, 'checkpoints')
  config['paths']['data_dir'] = os.path.join(model_path, 'datasets')
  config['preprocessing']['phoneme_symbols'] = phonemes
  config['preprocessing']['text_symbols'] = ''.join(graphemes)
  save_config(config, mod_config_file)

  preprocess(config_file = mod_config_file, train_data = train_data)
  train(config_file = os.path.join(model_path, 'config.yaml'))

def testing(model_path, test_dict):
  with open(test_dict, 'r', encoding='utf-8') as f:
    lines = f.readlines()

  lines = [l.replace('\n', '') for l in lines]
  splits = [l.split(' ', 1) for l in lines]
  splits = [[s[0],s[1].replace(' ','')] for s in splits]
  test_gr = [s[0] for s in splits if len(s)==2]
  test_ph = [s[1] for s in splits if len(s)==2]

  dct = [l.split(' ', 1) for l in lines]
  print('Testni grafemi: %s'%sorted(set(''.join([s[0] for s in dct]))))
  print('Testni fonemi: %s'%sorted(set(' '.join([s[1] for s in dct]).split(' '))))

  phonemizer = Phonemizer.from_checkpoint(os.path.join(model_path, 'checkpoints', 'best_model.pt'))
  result = phonemizer.phonemise_list(test_gr, lang='sl_SL')

  # Evaluation
  str_err = 0
  sym_err = 0
  print('\nNapačne pretvorbe na testnih nizih:')
  for gr, ref, pred in zip(test_gr, test_ph, result.phonemes):
    if pred != ref:
      # ~ import ipdb; ipdb.set_trace()
      str_err = str_err + 1
      sym_err = sym_err + lev(ref,pred)
      print('%s,\t%s,\t%s'%(gr,ref,pred))
  str_err = str_err/len(test_ph)*100
  sym_err = sym_err/len(''.join(test_ph))*100
  print('\nRezultati na %s:'%test_dict)
  print('WER=%.1f%%, PER=%.1f%%'%(str_err,sym_err))

def main(args):
  # ~ training(args.model, args.train_dict)
  testing(args.model, args.test_dict)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--model',
    type = str,
    default = './results/DeepPhonemizer/SingleCharacters/SloLeks_Validated_ASR_LemmaSplit_v2/'
  )
  parser.add_argument('--train_dict',
    type = str,
    default = '/storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_LemmaSplit_v2/sloleks_train_gfp.dict'
  )
  parser.add_argument('--test_dict',
    type = str,
    default = '/storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_LemmaSplit_v2/sloleks_test_gfp.dict'
  )
  args = parser.parse_args()
  
  main(args)

# CUDA_VISIBLE_DEVICES=1 python DeepPhonemizer_g2p_v3.py --model ./results/DeepPhonemizer/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/ --train_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_train_gfp.dict --test_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_test_gfp.dict
# CUDA_VISIBLE_DEVICES=1 python DeepPhonemizer_g2p_v3.py --model ./results/DeepPhonemizer/SingleCharacters/SloLeks_Validated_ASR_LemmaSplit_v2/ --train_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_LemmaSplit_v2/sloleks_train_gfp.dict --test_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_LemmaSplit_v2/sloleks_test_gfp.dict
# CUDA_VISIBLE_DEVICES=1 python DeepPhonemizer_g2p_v3.py --model ./results/DeepPhonemizer/SingleCharacters/SloLeks_Validated_TTS_RandomSplit/ --train_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_TTS_RandomSplit/sloleks_train_gfp.dict --test_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_TTS_RandomSplit/sloleks_test_gfp.dict
# CUDA_VISIBLE_DEVICES=1 python DeepPhonemizer_g2p_v3.py --model ./results/DeepPhonemizer/SingleCharacters/SloLeks_Validated_TTS_LemmaSplit_v2/ --train_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_TTS_LemmaSplit_v2/sloleks_train_gfp.dict --test_dict /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_TTS_LemmaSplit_v2/sloleks_test_gfp.dict

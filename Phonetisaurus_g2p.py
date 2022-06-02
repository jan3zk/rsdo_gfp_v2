import os
from Levenshtein import distance as lev
import argparse


def chunker(seq, size):
  return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def training(model_path, train_dict):
  os.makedirs(os.path.dirname(model_path), exist_ok=True)
  os.system('phonetisaurus train --model %s %s'%(os.path.join(model_path,'model.fst'), train_dict))

def testing(model_path, test_dict):
  with open(test_dict, 'r', encoding='utf-8') as f:
    lines = f.readlines()
  lines = [l.replace('\n', '') for l in lines]
  splits = [l.split(' ', 1) for l in lines]
  splits = [[s[0],s[1].replace(' ','')] for s in splits]
  test_gr = [s[0] for s in splits if len(s)==2]
  test_ph = [s[1] for s in splits if len(s)==2]

  pred_file = os.path.join(model_path,'phonetisaurus_predictions.txt')
  if os.path.exists(pred_file):
    os.remove(pred_file)
  for chk in chunker(test_gr,10000):
    chk = ' '.join(chk)
    os.system('phonetisaurus predict --model %s %s >> %s'%(os.path.join(model_path,'model.fst'), chk, pred_file))

  # Evalvacija
  with open(pred_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
  lines = [l.replace('\n', '') for l in lines]
  splits = [l.split(' ', 1) for l in lines]
  splits = [[s[0],s[1].replace(' ','')] for s in splits]
  pred_ph = [s[1] for s in splits if len(s)==2]

  str_err = 0
  sym_err = 0
  for ref, pred in zip(test_ph, pred_ph):
    if pred != ref:
      str_err = str_err + 1
      sym_err = sym_err + lev(ref,pred)
  str_err = str_err/len(test_ph)*100
  sym_err = sym_err/len(''.join(test_ph))*100
  print('Rezultati na %s:'%test_dict)
  print('WER=%.1f%%, PER=%.1f%%'%(str_err,sym_err))


def main(args):
  training(args.model, args.train_dict)
  testing(args.model, args.test_dict)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--model',
    type = str,
    default = './results/Phonetisaurus/SingleCharacters/SloLeks_Validated_TTS_LemmaSplit_v2'
  )
  parser.add_argument('--train_dict',
    type = str,
    default = '/storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_TTS_LemmaSplit_v2/sloleks_train_gfp.dict'
  )
  parser.add_argument('--test_dict',
    type = str,
    default = '/storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_TTS_LemmaSplit_v2/sloleks_test_gfp.dict'
  )
  args = parser.parse_args()
  
  main(args)

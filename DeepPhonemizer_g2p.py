import dp
import os
from dp.utils.io import read_config, save_config
from dp.preprocess import preprocess
from dp.train import train
from dp.phonemizer import Phonemizer

# Učenje
with open('gigafidaleks_asr_gfp_v1.dict', 'r', encoding='utf-8') as f:
  lines = f.readlines()

lines = [l.replace('\n', '') for l in lines]
splits = [l.split(' ', 1) for l in lines]
splits = [[s[0],s[1].replace(' ','')] for s in splits]
train_data = [('sl_SL', s[0], s[1]) for s in splits if len(s)==2]

preprocess(config_file='config.yaml', train_data=train_data)
train(config_file='config.yaml')

# Testiranje
with open('sofesleks_asr_gfp.dict', 'r', encoding='utf-8') as f:
  lines = f.readlines()

lines = [l.replace('\n', '') for l in lines]
splits = [l.split(' ', 1) for l in lines]
splits = [[s[0],s[1].replace(' ','')] for s in splits]
test_gr = [s[0] for s in splits if len(s)==2]
test_ph = [s[1] for s in splits if len(s)==2]

phonemizer = Phonemizer.from_checkpoint('checkpoints/best_model.pt')
result = phonemizer.phonemise_list(test_gr, lang='sl_SL')

err = 0
for res,ref in zip(result.phonemes, test_ph):
  if res != ref:
    err = err + 1
    print('reference: %s,\tpredicted: %s'%(ref,res))

print('Error rate = %.3f'%(err/len(test_ph)))



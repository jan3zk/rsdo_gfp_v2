# Grafemsko fonemska pretvorba (ver. 2)

Repozitorij vsebuje primer uporabe dveh postopkov grafemsko fonemske pretvorbe. Programske skripte omogočajo učenje in testiranje grafemsko fonemskega pretvornika na leksikonih za slovenski jezik. Učenje postopkov smo izvedli na leksikonu [gigafidaleks_asr_gfp_v1.dict](https://unilj-my.sharepoint.com/:u:/g/personal/janezkrfe_fe1_uni-lj_si/ETiBHKPuflhClH3yXc3lNdAB5wt5LmxFg-eXZHTpjtYrjA?e=9GIWvP), ki vsebuje 1440067 besedilnih nizov, testiranje pa na leksikonu [sofesleks_asr_gfp.dict](https://unilj-my.sharepoint.com/:u:/g/personal/janezkrfe_fe1_uni-lj_si/EZbQLPY1Gz5AvLnEzK4icnYBoYE1sow5gWa2XihVWtNwcg?e=63kCSh) s 1196 besedilnimi nizi.

## Grafemsko fonemski pretvornik Sequitur

Celotno orodje je dostopno na repozitoriju [https://github.com/sequitur-g2p/sequitur-g2p](https://github.com/sequitur-g2p/sequitur-g2p). Programske knjižnice, potrebne pri učenju in testiranju pretvornika sequitur, namestimo z ukazoma:
```
sudo apt install swig
sudo pip install git+https://github.com/sequitur-g2p/sequitur-g2p@master
```

Učenje pretvornika izvedemo preko spodnjih ukazov:
```
g2p.py --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-1 --viterbi -C -I 10
g2p.py --model model-1 --ramp-up --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-2 --viterbi -C -I 10
g2p.py --model model-2 --ramp-up --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-3 --viterbi -C -I 10
g2p.py --model model-3 --ramp-up --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-4 --viterbi -C -I 10
```
Preskus na testnem leksikonu izvedemo z ukazom:
```
g2p.py --model model-4 --test sofesleks_asr_gfp.dict
```
pri čemer se lahko poslužimo [predhodno naučenega modela](https://unilj-my.sharepoint.com/:u:/g/personal/janezkrfe_fe1_uni-lj_si/EWEPNOmBsCdKt7cGqJummYQBgygM8N_a3DDOj7vbpAx0mQ?e=mu1KPM).

## Grafemsko fonemski pretvornik DeepPhonemizer

Pretvornik DeepPhonemizer iz repozitorija [https://github.com/as-ideas/DeepPhonemizer](https://github.com/as-ideas/DeepPhonemizer) temelji na uporabi globokih nevronskih mrež. Namestitev knjižnice izvedemo z ukazom:
```
pip install deep-phonemizer
```
Proces učenja na leksikonu Gigafida in testiranje na leksikonu Sofesleks je povzeto v programski skripti [DeepPhonemizer_g2p.py](DeepPhonemizer_g2p.py). Datoteka [config.yaml](config.yaml) vsebuje nastavitve učne paramtrov in definicijo grafemov in fonemov za slovenski jezik. Test lahko izvedemo na [predhodno naučenem modelu](https://unilj-my.sharepoint.com/:u:/g/personal/janezkrfe_fe1_uni-lj_si/EbGvV5SxPOdPomwE3SrKBZIBUyycwXxbZePIuKVFxvhUQw?e=6aQ2W4).

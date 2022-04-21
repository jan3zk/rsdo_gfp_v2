sudo apt install swig
sudo pip install git+https://github.com/sequitur-g2p/sequitur-g2p@master

# Učenje pretvornika
g2p.py --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-1 --viterbi -C -I 10
g2p.py --model model-1 --ramp-up --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-2 --viterbi -C -I 10
g2p.py --model model-2 --ramp-up --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-3 --viterbi -C -I 10
g2p.py --model model-3 --ramp-up --train gigafidaleks_asr_gfp_v1.dict --devel 5% --write-model model-4 --viterbi -C -I 10

# Testiranje pretovrnika
g2p.py --model model-4 --test sofesleks_asr_gfp.dict

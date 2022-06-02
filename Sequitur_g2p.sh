#sudo apt install swig
#sudo pip install git+https://github.com/sequitur-g2p/sequitur-g2p@master

# ASR_RandomSplit:

# Training
g2p.py --train /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_train_gfp.dict --devel 5% --write-model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-1 
g2p.py --model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-1 --ramp-up --train /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_train_gfp.dict --devel 5% --write-model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-2
g2p.py --model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-2 --ramp-up --train /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_train_gfp.dict --devel 5% --write-model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-3
g2p.py --model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-3 --ramp-up --train /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_train_gfp.dict --devel 5% --write-model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-4

# Testing
g2p.py --model ${PWD}/results/Sequitur/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/model-ASR-RS-4 --test /storage/rsdo/jtdh/SingleCharacters/SloLeks_Validated_ASR_RandomSplit/sloleks_test_gfp.dict

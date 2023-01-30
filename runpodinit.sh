#!/bin/bash
#The intent here is to set up a server that can do the things the scripts require. I'm using runpod.io servers that already have pytorch installed 

apt update
apt --yes install libsndfile1-dev ffmpeg emacs python3.9-dev nq

export BASEDIR=/workspace
export TORTOISE_MODELS_DIR=$BASEDIR/models

cd $BASEDIR
mkdir inputs
mkdir logs
mkdir outputs
mkdir models

python -m pip install tqdm rotary_embedding_torch
python -m pip install transformers==4.19
python -m pip install tokenizers inflect
python -m pip install progressbar einops unidecode scipy
python -m pip install librosa numpy==1.20.0 numba==0.48.0
python -m pip install torchaudio
python -m pip install threadpoolctl
python -m pip install llvmlite
python -m pip install wikipedia
python -m pip install appdirs
python -m pip install Cython pynini
python -m pip install git+https://github.com/NVIDIA/NeMo.git@main#egg=nemo_toolkit[nlp]

git clone https://github.com/neonbjb/tortoise-tts
git clone https://github.com/NVIDIA/NeMo-text-processing/
cd tortoise-tts

python -m pip install .

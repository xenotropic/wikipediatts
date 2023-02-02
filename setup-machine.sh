#!/bin/bash
#The intent here is to set up a server that can do the things the scripts require. I'm using runpod.io servers that already have pytorch installed; they use /workspace as a root working directory. Change BASEDIR as appropriate or your setup. 

apt update
apt --yes install libsndfile1-dev ffmpeg emacs python3.9-dev nq less task-spooler

export BASEDIR=/notebooks
export TORTOISE_MODELS_DIR=$BASEDIR/models
export NQDIR=$BASEDIR/outputs
cd $BASEDIR

python -m pip install -r tortoise-tts/requirements.txt
python -m pip install wikipedia Cython pynini
python -m pip install git+https://github.com/NVIDIA/NeMo.git@main#egg=nemo_toolkit[nlp]

cd tortoise-tts

python -m pip install .

cd $BASEDIR/wikipedia-tts

#!/bin/bash
cd $BASEDIR
WIKIARTICLE=$1
VOICE=train_winston
TORTOISE_MODELS_DIR=$BASEDIR/models
mkdir $BASEDIR/outputs/$WIKIARTICLE
python3 $BASEDIR/tortoise-tts/tortoise/read.py --model_dir $BASEDIR/models --textfile $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt --voice train_e --preset=fast --output_path=$BASEDIR/outputs/$WIKIARTICLE > /$BASEDIR/logs/$WIKIARTICLE.log 2>&1 &
ffmpeg -i $BASEDIR/outputs/$WIKIARTICLE/$VOICE/combined.wav $BASEDIR/outputs/$WIKIARTICLE/$VOICE/$WIKIARTICLE.mp3 -metadata title="Wikipedia article on $WIKIARTICLE read by a text to speech voice, see https://github.com/xenotropic/wikipedia-tts/"

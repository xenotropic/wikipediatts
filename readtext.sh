#!/bin/bash
cd $BASEDIR
export TMPDIR=$BASEDIR/logs/
export WIKIARTICLE=$1
export VOICE=train_winston
export TORTOISE_MODELS_DIR=$BASEDIR/models
mkdir $BASEDIR/outputs/$WIKIARTICLE
tsp sh -c "python3.9 $BASEDIR/tortoise-tts/tortoise/read.py --model_dir $BASEDIR/models --textfile $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt --voice $VOICE --preset=fast --output_path=$BASEDIR/outputs/$WIKIARTICLE > /$BASEDIR/logs/$WIKIARTICLE.log 2>&1"
tsp -d sh -c 'ffmpeg -i $BASEDIR/outputs/$WIKIARTICLE/$VOICE/combined.wav $BASEDIR/outputs/$WIKIARTICLE/$VOICE/$WIKIARTICLE.mp3 -metadata title="Wikipedia article on $WIKIARTICLE read by a text to speech voice, content CC-BY-SA see https://github.com/xenotropic/wikipedia-tts/ for more info" >> /$BASEDIR/logs/$WIKIARTICLE.log 2>&1' 
tsp -d sh -c 'scp $BASEDIR/outputs/$WIKIARTICLE/$VOICE/$WIKIARTICLE.mp3 joe@dune:www/wcast.me/tts/'

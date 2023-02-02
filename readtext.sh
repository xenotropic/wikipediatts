#!/bin/bash
cd $BASEDIR
WIKIARTICLE=$1
mkdir $BASEDIR/outputs/$WIKIARTICLE
python $BASEDIR/tortoise-tts/tortoise/read.py --model_dir $BASEDIR/models --textfile $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt --voice train_winston --preset=fast --output_path=$BASEDIR/outputs/$WIKIARTICLE > /$BASEDIR/logs/$WIKIARTICLE.log 2>&1 &

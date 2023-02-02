#!/bin/bash
cd $BASEDIR
WIKIARTICLE=$1
mkdir $BASEDIR/inputs/$WIKIARTICLE
python wikipedia-tts/wikiparse.py $WIKIARTICLE > $BASEDIR/inputs/$WIKIARTICLE.txt
python wikipedia-tts/wikiparse.py $WIKIARTICLE > $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt
nq python $BASEDIR/tortoise-tts/tortoise/read.py --model_dir $BASEDIR/models --textfile $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt --voice train_e --preset=fast --output_path=$BASEDIR/outputs > /$BASEDIR/logs/$WIKIARTICLE.log 2>&1 

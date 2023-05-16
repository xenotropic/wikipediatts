#!/bin/bash
cd $BASEDIR
TMPDIR=$BASEDIR/logs/
WIKIARTICLE=$1
VOICE=jmm5
MODEL=insert_me
CVVP=1.0
DESTINATION=insert_me
OTHERPARAMS="--original_tortoise True --vocoder BigVGAN --preset=high_quality"
mkdir $BASEDIR/outputs/$WIKIARTICLE
python3.9 ~/tts/tortoise-tts-fast/scripts/tortoise_tts.py --voice=$VOICE  --output_dir=$BASEDIR/outputs/$WIKIARTICLE --cvvp_amount $CVVP --voicefixer False $OTHERPARAMS --ar_checkpoint=$MODEL <  $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt && ffmpeg-normalize $BASEDIR/outputs/$WIKIARTICLE/${VOICE}_combined.wav -c:a mp3 -t -16 -pr -o $BASEDIR/outputs/$WIKIARTICLE/$WIKIARTICLE.mp3 && scp $BASEDIR/outputs/$WIKIARTICLE/$WIKIARTICLE.mp3 $DESTINATION
cat >> $TMPDIR/metalog "$WIKIARTICLE, $VOICE, $MODEL, $CCVP, $OTHERPARAMS"



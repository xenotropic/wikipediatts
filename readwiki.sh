#!/bin/bash
cd $BASEDIR
WIKIARTICLE=$1
mkdir $BASEDIR/inputs/$WIKIARTICLE
python wikipedia-tts/wikiparse.py $WIKIARTICLE > $BASEDIR/inputs/$WIKIARTICLE/$WIKIARTICLE.txt

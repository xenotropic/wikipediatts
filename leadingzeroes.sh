#!/bin/bash
for a in [0-9]*.wav; do
    mv $a `printf %04d.%s ${a%.*} ${a##*.}`
done

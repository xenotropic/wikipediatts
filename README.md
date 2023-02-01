# wikipedia-tts
Scripts gluing together TorToiSe with text preprocessing with the goal of getting clean audio readings of Wikipedia articles. Waaay alpha use with caution.

## Setup.

I'm using this with runpods.io, so the intent here is to set up and run on a temporary machine with root access. 

The initial command to your empty server (as sudo or root) is

`cd /workspace && git clone https://github.com/xenotropic/wikipedia-tts && source ./wikipedia-tts/runpodinit.sh`

Where /workspace is whatever directory you want your repos and models in. If it is *not* /workspace also modify the BASEDIR set in runpodinit.sh before you run it. 

## Voices. 

The voices in the feed are based on [LibriTTS voices](https://www.openslr.org/60/). Althugh I may use a single voice in some articles in the podcast feed, eventually I will probably blend two or more voices, so they aren't the voice of any single person. 
 
To add more voices they have to be in 22050 Hz 32-bit float format. One can do this with:

`ffmpeg -i 3.wav -ar 22050 -c:a pcm_f32le 3o.wav`

## To-do

Most of what I'm doing is refining what happens in the text preprocessor to help the tts engine with things it does not say correctly by default. Eventually many of these may well be fixed by larger training sets, but for now I'm doing the simpler task of just making the text "easy to say", since tortoise does quite well saying things phonetically.  I recently added NVidia's [NeMo text processing](https://github.com/NVIDIA/NeMo-text-processing/) which may handle some of these.

- [ ] Write a script that runs the text preprocessing and then the appropriate read.py command to tortoise on the resulting text file
- [ ] Copy extra voices from this repo into the tortoise voices dir
- [ ] Reduce repeats -- sometimes Tortoise "phrase stutters" saying the same few words two or three times. Have to tinker with TorToiSe params, see its [#237](https://github.com/neonbjb/tortoise-tts/issues/237)
- [ ] Separate acronyms -- so it says FBI as F B I rather than Fubeye
- [ ] Roman numeral handling 
- [ ] Replace m-dashes with n-dashes in year ranges
- [ ] Remove n-dashes, seems to just cause a pause where none is expected
- [ ] % to "percent"
- [ ] Remove footnoes -- most are being omitted by virtue of being in brackets (which Tortose ignores) but pincites to pages are outside of the brackets; might as well remove them all
- [ ] Remove brackets in quotes -- this is a common pattern to "fix" a quotation so it is readable out of its context, but then tortoise skips the bracketed text which is bad
- [ ] Country pronouciation -- Tortoise does not know how to say country names reliably, so like Czechoslovakia and Argentina don't come out right. Its training set was on out-of-copyright books so it's a large body of words it is not familiar with. 
- [ ] Common abbreviations -- e.g., kmh to "kilometers per hour", need a dictionary of these

# wikipedia-tts
Scripts gluing together TorToiSe with text preprocessing with the goal of getting clean audio readings of Wikipedia articles. Waaay alpha use with caution. You can listen to example outputs, as a podcast RSS feed, at https://morris.cloud/wikipedia-tts/ 

## Setup.

I'm using this with runpods.io, so the intent here is to set up and run on a temporary machine with root access. 

The initial command to your empty server (as sudo or root) is

`export BASEDIR=/notebooks && cd $BASEDIR && git clone https://github.com/xenotropic/wikipedia-tts && source ./wikipedia-tts/setup-all.sh`

Where /notebooks is whatever directory you want your repos and models in. ("/notebooks" happens to be what paperspace uses) 

## Voices. 

The voices in the feed are based on [LibriTTS voices](https://www.openslr.org/60/).  
 
To add more voices they have to be in 22050 Hz 32-bit float format. One can do this with:

`ffmpeg -i 3.wav -ar 22050 -c:a pcm_f32le 3o.wav`

## To-do

Most of what I'm doing is making scripts that set up a new machine like one gets from paperspace or runpods.io; and pipelining from Wikipedia into Tortoise. The primary task at the moment I'm working on is text normalization -- changing the text so it can be said literally by the Tortoise TTS engine.  I recently added NVidia's [NeMo text processing](https://github.com/NVIDIA/NeMo-text-processing/) which is handling a lot of the text normalization.At least at an initial glance doesn't seem perfect and will likely require additional text processing.

- [x] Write a script that runs the text preprocessing and then the appropriate read.py command to tortoise on the resulting text file
- [x] Copy extra voices from this repo into the tortoise voices dir
- [ ] Ongoing search for things NeMo misses, e.g., getting some instances of "Kilometers per H"
- [ ] Reduce repeats -- sometimes Tortoise "phrase stutters" saying the same few words two or three times. Have to tinker with TorToiSe params, see its [#237](https://github.com/neonbjb/tortoise-tts/issues/237)
- [x] Separate acronyms -- so it says FBI as F B I rather than Fubeye
- [ ] Roman numeral handling (Nemo?)
- [ ] Replace m-dashes with n-dashes in year ranges
- [ ] Remove n-dashes, seems to just cause a pause where none is expected
- [ ] % to "percent"
- [ ] Remove footnotes -- most are being omitted by virtue of being in brackets (which Tortose ignores) but pincites to pages are outside of the brackets; might as well remove them all
- [ ] Remove brackets in quotes -- this is a common pattern to "fix" a quotation so it is readable out of its context, but then tortoise skips the bracketed text which is bad
- [ ] Country pronouciation -- Tortoise does not know how to say country names reliably, so like Czechoslovakia and Argentina don't come out right. Its training set was on out-of-copyright books so it's a large body of words it is not familiar with. 


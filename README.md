# wikipedia-tts
Scripts gluing together [TorToiSe](https://github.com/neonbjb/tortoise-tts) with [Nvidia's NeMo](https://github.com/NVIDIA/NeMo-text-processing) and other text preprocessing with the goal of getting clean audio readings of Wikipedia articles. You can listen to example outputs, as a podcast RSS feed, at https://morris.cloud/wikipedia-tts/ . Theoretically they should be getting better over time, as I improve the text preprocessing pipeline. 

## Setup.

TorToiSe requires an Nvidia GPU, and in my experience it needs one with 16GB of RAM to run reliably. I'm using this with paperspace gradient, so the intent here is to set up and run on a temporary machine with root access. If you are installing this on your own personal machine, there are apt install commands in the setup, but you might want to review first, and you will have to use su. 

The initial command to your empty server (as sudo or root) is

`export BASEDIR=/notebooks && cd $BASEDIR && git clone https://github.com/xenotropic/wikipedia-tts && source ./wikipedia-tts/setup-all.sh`

Where /notebooks is whatever directory you want your repos and models in. ("/notebooks" happens to be what paperspace uses) 

setup-machine.sh  is for where the machine has been stopped and started again (i.e., apt and pip dependencies lost), but where the contents of $BASEDIR were preserved. 

## Rendering Articles. 

Currently article rendering is in two stages, with some human intervention advised in between. Both take one argument, which is the title of the article as it appears in the URL: 

`textprep.sh` prepares the text and places it in the $BASEDIR/input directory. Watch for any over-length sentences, these need to be further broken up with a pipe symbol | . You may wish to also do other text processing by hand: removing non-Roman characters; replacing unusual words that are not pronounced the way they appear, with a phonetic spelling; making sure that all number ranges are rendered correctly, and scientific units.

`readtext.sh` sends the text off to TorToiSe's read.py function with various parameters set. 

So if you wanted to generate a reading of  the Wikipedia article on Barack Obama, you'd run

`textprep.sh Barack_Obama`

then you'd edit $BASEDIR/inputs/Barack_Obama/Barack_Obama.txt with yor favorite text editor, then run

`readtext.sh Barack_Obama`

If a run is completed, you get "complete.wav", which is the output, in a subdirectory of $BASEDIR/outputs. 

If a run is interrupted, then you are left with a bunch of .wav files, one per sentence. I use leadingzeroes.sh to add leading zeroes to them so the shell gives them in order; then run "sox *.wav complete.wav" to get a file with them altogether. Then 
`ffmpeg -i complete.wav [outputfile].mp3" to get an mp3.

The goal is to get the text preprocessing good enough that the intermediate step of human editing isn't necessary.

## Voices. 

The voices in this repo, and in the feed are from [LibriTTS voices](https://www.openslr.org/60/).  
 
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
- [ ] Strip initial phonetic spelling if present, or ensure not expanded as an acronym
- [ ] Country pronouciation -- Tortoise does not know how to say country names reliably, so like Czechoslovakia and Argentina don't come out right. Its training set was on out-of-copyright books so it's a large body of words it is not familiar with. 


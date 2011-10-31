#! /bin/zsh
pd -jack -channels 2 -alsamidi -mididev 2 -open ~/code/pippi/pippi.pd -send "pd dsp 1" 

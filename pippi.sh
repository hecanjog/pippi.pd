#! /bin/zsh
screen pd -nogui -jack -channels 2 -alsamidi -mididev 2 -open ~/code/pippi/_pip.pd -send "pd dsp 1" 

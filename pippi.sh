#! /bin/zsh
#/usr/bin/jackd -P 70 -r -dalsa -r44100 -p2048 -n2 -D -Chw:0,0 -Phw:0 -Xseq &
screen pd -nogui -jack -channels 2 -alsamidi -mididev 2 -open ~/code/pippi/_pip.pd -send "pd dsp 1" 

#! /bin/zsh

# start jack
/usr/bin/jackd -P 70 -R -dalsa -r44100 -p2048 -n2 -D -Chw:0,0 -Phw:0 -Xseq &
/usr/bin/qjackctl & sleep 2 ;

# start pd
pd -rt -jack -channels 2 -alsamidi -mididev 2 -open ~/.aaahcjpd/_pip/_pip.pd -send "pd dsp 1" & sleep 2 ;

# input connections
jack_connect system:capture_1 pure_data_0:input0 ;
jack_connect system:capture_2 pure_data_0:input1 ;

# output connections
jack_connect pure_data_0:output0 system:playback_1 ;
jack_connect pure_data_0:output1 system:playback_2

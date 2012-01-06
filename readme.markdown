Pippi is some shit I use when I perform.

It's intended to be used from the linux console and makes
use of the following software:

- GNU screen or tmux (optional, but nice!)
- PureData (vanilla) with the pdlua and zexy libraries - pd-extened has both of these preinstalled last I checked.
- Python

Quick start:

Open pd in nogui mode with the included shell script or by running this command:

    pd -nogui -open /path/to/pippi.pd -send "pd dsp 1"

In another terminal, launch the pippi console:  
    
    python /path/to/pippi/console.py

To open a connection to pd from the pippi console type

    pd c

To turn the overtones up type

    o v 9

To retune the three groups to 220, 440, and 660 hz and use the first 6 partials for each voice

    o af 220, bf 440, cf 660, p 1 2 3 4 5 6

See console.py for more!

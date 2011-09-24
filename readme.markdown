Pippi is some shit I use when I perform.

It's intended to be used from the linux console and makes
use of the following software:

- GNU Screen (optional, but nice!)
- PureData (vanilla) with the pdlua and zexy libraries
- Python
- Jack (optional)


Quick start:

To open pippi in a split screen, drop this in your .screenrc

    screen -t pd 0 sh /path/to/pippi/pippi.sh 
    split
    focus up
    screen -t pippi 1 python2 /path/to/pippi/console.py

To open a connection to pd from the pippi console type
    pd c

To turn the overtones up type
    o v 9

See console.py for more!

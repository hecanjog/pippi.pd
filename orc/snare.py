import dsp
import tune

def play(args):
    snd = False
    reps = 8
    length = dsp.stf(20)
    volume = 0.1 
    octave = 4 
    note = 'd'
    quality = tune.major
    m = 1
    width = 0
    waveform = 'sine'

    scale = [1,5,8]
    wtypes = ['sine', 'phasor', 'line', 'saw']

    for arg in args:
        a = arg.split(':')

        if a[0] == 't':
            length = int(a[1])

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 'r':
            reps = int(a[1])

        if a[0] == 'n':
            note = a[1]

        if a[0] == 'm':
            m = float(a[1])

        if a[0] == 'w':
            width = dsp.mstf(float(a[1]))

        if a[0] == 'q':
            if a[1] == 'M':
                quality = tune.major
            elif a[1] == 'm':
                quality = tune.minor
            else:
                quality = tune.major

        if a[0] == 'g':
            glitch = True

        if a[0] == 's':
            if a[1] == 'c':
                snd = dsp.read('sounds/clapshake.wav').data
            elif a[1] == 'h':
                snd = dsp.read('sounds/hihat.wav').data
            elif a[1] == 's':
                snd = dsp.read('sounds/snare.wav').data
            elif a[1] == 'k':
                snd = dsp.read('sounds/kick.wav').data
            else:
                snd = dsp.read('sounds/hihat.wav').data


    out = ''

    if(w <= 11):
        w = 11

    width = dsp.mstf(t)
    for h in range(reps):
        s = dsp.cut(snd, dsp.randint(0, 100), w)
        out += dsp.pad(s, 0, width - dsp.flen(s))
    
    out = dsp.env(out, 'gauss')

    return dsp.cache(dsp.amp(out, volume))

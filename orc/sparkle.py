import dsp
import tune

def play(args):
    length = dsp.stf(20)
    volume = 0.1 
    octave = 4 
    note = 'd'
    quality = tune.major
    m = 1
    width = 0
    waveform = 'sine'

    harmonics = [1,2]
    scale = [1,5,8]
    wtypes = ['sine', 'phasor', 'line', 'saw']
    ratios = tune.terry

    for arg in args:
        a = arg.split(':')

        if a[0] == 't':
            length = dsp.stf(float(a[1]))

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 'o':
            octave = int(a[1])

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

        if a[0] == 'h':
            harmonics = [int(s) for s in a[1].split('.')]

        if a[0] == 'g':
            glitch = True

        if a[0] == 'wf':
            waveform = a[1]

        if a[0] == 'tr':
            if a[1] == 'young':
                ratios = tune.young
            elif a[1] == 'terry':
                ratios = tune.terry


    tones = []
    m *= 1.0
    for i in range(dsp.randint(2,4)):
        freq = tune.step(i, note, octave, dsp.randshuffle(scale), quality, ratios)

        snds = [ dsp.tone(length, freq * h, waveform) for h in harmonics ]
        for snd in snds:
            snd = dsp.vsplit(snd, dsp.mstf(10 * m), dsp.mstf(100 * m))
            if width != 0:
                for ii, s in enumerate(snd):
                    olen = dsp.flen(s)
                    s = dsp.cut(s, 0, width)
                    s = dsp.pad(s, 0, olen - dsp.flen(s)) 
                    snd[ii] = s

            snd = [ dsp.env(s, dsp.randchoose(wtypes)) for s in snd ]
            snd = [ dsp.pan(s, dsp.rand()) for s in snd ]
            snd = [ dsp.amp(s, dsp.rand()) for s in snd ]
            snd = ''.join(snd)

            tones += [ snd ]

    out = dsp.mix(tones)
    out = dsp.env(out, 'gauss')

    return dsp.cache(dsp.amp(out, volume))

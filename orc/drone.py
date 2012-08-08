import dsp
import tune

def play(args):
    length = dsp.stf(20)
    volume = 0.2 
    octave = 2 
    note = 'd'
    quality = tune.major
    glitch = False
    waveform = 'sine'
    ratios = tune.terry

    harmonics = [1,2]
    scale = [1,8]
    wtypes = ['sine', 'phasor', 'line', 'saw']

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

        if a[0] == 'q':
            if a[1] == 'M':
                quality = tune.major
            elif a[1] == 'm':
                quality = tune.minor
            else:
                quality = tune.major

        if a[0] == 'tr':
            if a[1] == 'young':
                ratios = tune.young
            elif a[1] == 'terry':
                ratios = tune.terry

        if a[0] == 'h':
            harmonics = [int(s) for s in a[1].split('.')]

        if a[0] == 'g':
            glitch = True

        if a[0] == 'wf':
            waveform = a[1]

    tones = []
    for i in range(dsp.randint(2,4)):
        freq = tune.step(i, note, octave, dsp.randshuffle(scale), quality, ratios)

        snds = [ dsp.tone(length, freq * h, waveform) for h in harmonics ]

        snds = [ dsp.env(s, dsp.randchoose(wtypes), highval=dsp.rand(0.2, 0.4)) for s in snds ]
        snds = [ dsp.pan(s, dsp.rand()) for s in snds ]

        tones += [ dsp.mix(snds) ]

    out = dsp.mix(tones)

    if glitch:
        inlen = dsp.flen(out) * 0.25
        instart = 0

        midlen = dsp.flen(out) * 0.5
        midstart = inlen

        endlen = dsp.flen(out) - (inlen + midlen)
        endstart = inlen + midlen
        
        outin = dsp.cut(out, instart, inlen)
        outmid = dsp.cut(out, midstart, midlen)
        outend = dsp.cut(out, endstart, endlen)

        out = "%s%s%s" % (dsp.env(outin, 'line'), outmid, dsp.env(outend, 'phasor'))
    else:
        out = dsp.env(out, 'gauss')

    return dsp.cache(dsp.amp(out, volume))

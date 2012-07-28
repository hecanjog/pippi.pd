import dsp
import tune

def play(args):
    length = dsp.stf(dsp.rand(5, 10))
    volume = 0.2 
    octave = 2 
    note = 'd'
    quality = tune.major
    reps = dsp.randint(3, 11)
    glitch = False
    superglitch = False
    pulse = False

    rhodes = dsp.read('sounds/220rhodes.wav').data

    #scale = [1,3,5,4]
    scale = [1,5,8,6]

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

        if a[0] == 'r':
            reps = int(a[1])

        if a[0] == 'p':
            pulse = True

        if a[0] == 'g':
            glitch = True

        if a[0] == 'gg':
            glitch = True
            superglitch = True

        if a[0] == 's':
            scale = [int(s) for s in a[1].split('.')]

    out = ''
    for i in range(reps):
        freq = tune.step(i, note, octave, scale, quality)
        diff = freq / 440.0

        n = dsp.transpose(rhodes, diff)
        n = dsp.fill(n, length)

        o = [dsp.tone(length, freq * i * 0.5) for i in range(4)]
        o = [dsp.env(oo) for oo in o]
        o = [dsp.pan(oo, dsp.rand()) for oo in o]
        o = dsp.mix([dsp.amp(oo, dsp.rand(0.05, 0.1)) for oo in o])
        out += dsp.mix([n, o])

    if glitch == True:
        if superglitch == True:
            mlen = dsp.mstf(100)
        else:
            mlen = dsp.flen(out) / 8

        out = dsp.vsplit(out, dsp.mstf(1), mlen)
        out = [dsp.pan(o, dsp.rand()) for o in out]
        out = ''.join(dsp.randshuffle(out))

    if pulse == True:
        plen = dsp.mstf(dsp.rand(80, 500))
        out = dsp.split(out, plen)
        mpul = len(out) / dsp.randint(4, 8)

        out = [dsp.env(o) * mpul for i, o in enumerate(out) if i % mpul == 0]
        opads = dsp.wavetable('sine', len(out), dsp.rand(plen * 0.25, plen))
        out = [dsp.pad(o, 0, int(opads[i])) for i, o in enumerate(out)]
        out = dsp.env(''.join(out))

    return dsp.cache(dsp.amp(out, volume))

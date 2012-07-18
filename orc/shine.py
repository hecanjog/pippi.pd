import dsp
import tune

def play(args):
    length = dsp.stf(3)
    volume = 0.2 
    octave = 3
    note = 'd'
    reps = 30 
    nlen = dsp.mstf(5000)

    rhodes = dsp.read('sounds/220rhodes.wav').data

    scale = [1,3,5,4]

    for arg in args:
        a = arg.split(':')

        if a[0] == 'b':
            nlen = dsp.mstf(float(a[1]))

        if a[0] == 't':
            length = dsp.stf(float(a[1]))

        if a[0] == 'v':
            volume = float(a[1]) / 100.0

        if a[0] == 'o':
            octave = int(a[1])

        if a[0] == 'n':
            note = a[1]

        if a[0] == 'r':
            reps = int(a[1])

        if a[0] == 's':
            scale = [int(s) for s in a[1].split('.')]

    out = ''
    for i in range(reps):
        freq = tune.step(i, note, octave, scale)
        diff = freq / 440.0

        n = dsp.transpose(rhodes, diff)
        n = dsp.fill(n, nlen)

        o = [dsp.tone(nlen, freq * i * 0.5) for i in range(4)]
        o = [dsp.env(oo) for oo in o]
        o = [dsp.pan(oo, dsp.rand()) for oo in o]
        o = dsp.mix([dsp.amp(oo, dsp.rand(0.05, 0.1)) for oo in o])
        out += dsp.mix([n, o])

    return dsp.cache(out)

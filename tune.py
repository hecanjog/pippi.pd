a0 = 27.5 

just = [
    (1.0, 1.0),     # P1
    (16.0, 15.0),   # m2
    (9.0, 8.0),     # M2
    (6.0, 5.0),     # m3
    (5.0, 4.0),     # M3
    (4.0, 3.0),     # P4
    (45.0, 32.0),   # TT
    (3.0, 2.0),     # P5
    (8.0, 5.0),     # m6
    (5.0, 3.0),     # M6
    (9.0, 5.0),     # m7
    (15.0, 8.0),    # M7
]

terry = [
    (1.0, 1.0),     # P1
    (16.0, 15.0),   # m2
    (10.0, 9.0),    # M2
    (6.0, 5.0),     # m3
    (5.0, 4.0),     # M3
    (4.0, 3.0),     # P4
    (64.0, 45.0),   # TT
    (3.0, 2.0),     # P5
    (8.0, 5.0),     # m6
    (27.0, 16.0),   # M6
    (16.0, 9.0),    # m7
    (15.0, 8.0),    # M7
]

young = [
    (1.0, 1.0),       # P1 0
    (567.0, 512.0),   # m2 1
    (9.0, 8.0),       # M2 2
    (147.0, 128.0),   # m3 3
    (21.0, 16.0),     # M3 4
    (1323.0, 1024.0), # P4 5
    (189.0, 128.0),   # TT 6
    (3.0, 2.0),       # P5 7
    (49.0, 32.0),     # m6 8
    (7.0, 4.0),       # M6 9
    (441.0, 256.0),   # m7 10
    (63.0, 32.0),     # M7 11
]

major = [0, 2, 4, 5, 7, 9, 11]
minor = [0, 2, 3, 5, 7, 8, 10]

notes = [ 
    ['a'], 
    ['a#', 'bb'], 
    ['b'], 
    ['c'], 
    ['c#', 'db'], 
    ['d'], 
    ['d#', 'eb'], 
    ['e'], 
    ['f'], 
    ['f#', 'gb'], 
    ['g'], 
    ['g#', 'ab'], 
]

def nti(note):
    """ Note to index
            returns the index of enharmonic note names
            or False if not found
    """
    for d, n in enumerate(notes):
        for e in n:
            if e == note:
                return d

    return False 

def ntf(note, octave=4, ratios=terry):
    """ Note to freq 
    """
    return ratios[nti(note)][0] / ratios[nti(note)][1] * (a0 * (2.0**octave))

def step(degree=0, root='c', octave=4, scale=[1,3,5,8], quality=major, ratios=terry):
    diatonic = scale[degree % len(scale) - 1]
    chromatic = quality[diatonic % len(quality) - 1]

    pitch = ratios[chromatic][0] / ratios[chromatic][1]
    pitch *= octave + int(diatonic / len(quality))
    pitch *= ntf(root, octave, ratios)

    return pitch

def scale(pitches=[1,3,5], quality=major):
    return [quality[p - 1] for p in pitches]

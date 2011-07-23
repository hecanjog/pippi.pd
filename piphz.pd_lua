local PipHz = pd.Class:new():register("piphz")

function PipHz:initialize(sel, atoms)
    self.inlets = 1 
    self.outlets = 2 
    self.voices = {} 
    self.base_hz = 65.406 

    self.ratios = {
            {1, 1},
            {16, 15},
            {9, 8},
            {6, 5},
            {5, 4},
            {4, 3},
            {45, 32},
            {3, 2},
            {8, 5},
            {5, 3},
            {9, 5},
            {15, 8}
    }

    if type(atoms[1]) == "number" then self.base_hz = atoms[1] end

    for voice_num = 1, self.outlets do
        table.insert(self.voices, {voice_num, 440, 0, 1})
    end

    return true
end

function PipHz:in_1(sel, atoms)
    voice_index = atoms[1]
    amp = atoms[3]
    pitch = atoms[2]

    scale_degree = pitch % 12
    base_octave = pitch - scale_degree
    octave_offset = base_octave / 12
    octave_offset = 2 ^ octave_offset

    ratio = self.ratios[scale_degree + 1]
    ratio = ratio[1] / ratio[2]
    hz = (self.base_hz / 8) * (octave_offset * ratio)

    self.voices[atoms[1]] = {voice_index, hz, amp, octave_offset * ratio}

    if amp > 0 then
        self:outlet(1, sel, {atoms[1], self.voices[atoms[1]][4]})
        self:outlet(2, sel, self.voices[atoms[1]])
    end
end

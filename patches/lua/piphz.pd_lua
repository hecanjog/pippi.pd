local PipHz = pd.Class:new():register("piphz")

function PipHz:initialize(sel, atoms)
    self.inlets = 2 
    self.outlets = 4 
    self.voices = {} 
    self.base_hz = 240.0
    self.samp_hz = 110

    self.ratios = {
            {1, 1},
            {16, 15},
            {10, 9},
            {6, 5},
            {5, 4},
            {4, 3},
            {64, 45},
            {3, 2},
            {8, 5},
            {27, 16},
            {16, 9},
            {15, 8}
    }

    if type(atoms[1]) == "number" then
        self.base_hz = atoms[1]
    end

    if type(atoms[2]) == "number" then
        self.samp_hz = atoms[2]
    end

    pd.post("Tuning to: " .. tostring(self.base_hz))

    return true
end

function PipHz:in_2_float(hz)
    if type(hz) == "number" then
            self.base_hz = hz 
    end
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
    hz = (self.base_hz / 32) * (octave_offset * ratio)

    hz_diff = self.base_hz / self.samp_hz
    speed = (octave_offset * ratio * hz_diff) / 32

    self.voices[atoms[1]] = {voice_index, hz, amp, speed}

    if amp > 0 then
        amp = 1
        self:outlet(3, sel, {voice_index, amp})
        self:outlet(1, sel, {atoms[1], self.voices[atoms[1]][4]})
        self:outlet(2, sel, self.voices[atoms[1]])
    else
        self:outlet(4, sel, {voice_index, amp})
    end

end

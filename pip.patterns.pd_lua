local PipPatterns = pd.Class:new():register("pip.patterns")

function PipPatterns:initialize(classname, atoms)
    self.inlets = 4 
    self.outlets = 1
    self.beat = 2000
    self.current_pattern = 1
    self.current_step = 1
    self.max_step = 17

    if type(atoms[1]) == "number" then
        self.beat = atoms[1]
    end

    if type(atoms[2]) == "number" then
        self.current_pattern = atoms[2]
    end

    -- TODO: do this in a more elegant way...
    self.patterns = {
            {1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0},
            {1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1},
            {1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1},
            {0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0},
            {1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0},
            {1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0},
            {1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1},
            {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
    }

    self.patterns[0] = {1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0}

    return true

end

function PipPatterns:postinitialize()
    self.metro = pd.Clock:new():register(self, "trig")
end

function PipPatterns:finalize()
    self.metro:destruct()
end

function PipPatterns:in_1_bang()
    self.current_step = 1
    self:trig()
end

function PipPatterns:in_2_float(ed)
    if type(ed) == "number" then
        self.beat = ed
    end
end

function PipPatterns:in_3_float(pattern_number)
    if type(pattern_number) == "number" then
        self.current_pattern = pattern_number
    end
end

function PipPatterns:in_4_float(step_number)
    if type(step_number) == "number" then
        self.current_step = step_number
    end
end

function PipPatterns:calculate()
    self.metro:delay(self.beat / 16)
end

function PipPatterns:in_1_stop()
    self.metro:unset()
end

function PipPatterns:trig()
    if self.patterns[self.current_pattern][self.current_step] == 1 then
        self:outlet(1, "bang", {})
    end
    
    if self.current_step < self.max_step then
        self.current_step = self.current_step + 1
    else
        self.current_step = 1
    end

    self:calculate()
end


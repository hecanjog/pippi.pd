local PipMetro = pd.Class:new():register("pip.metro")

function PipMetro:initialize(classname, atoms)
    self.inlets = 1 
    self.outlets = 2 
    self.ed = 1000
    self.beats = 2

    if type(atoms[1]) == "number" then
        self.ed = atoms[1]
    end

    if type(atoms[2]) == "number" then
        self.beats = atoms[2]
    end

    return true

end

function PipMetro:postinitialize()
    self.metro = pd.Clock:new():register(self, "trig")
end

function PipMetro:finalize()
    self.metro:destruct()
end

function PipMetro:in_1_bang()
    self:trig()
end

function PipMetro:in_1_float(ed)
    ed = (60000 / ed ) * self.beats 
    self.ed = ed
end

function PipMetro:in_1_stop()
    self.metro:unset()
end

function PipMetro:trig()
    self:outlet(1, "bang", {})
    self:outlet(2, "float", { self.ed })

    self.metro:delay(self.ed)
end

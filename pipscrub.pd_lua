local PipScrub = pd.Class:new():register("pipscrub")

function PipScrub:initialize(sel, atoms)
    self.inlets = 1
    self.outlets = 1
    self.size = 44100

    if type(atoms[1]) == "number" then
        self.size = atoms[1]
    end

    return true
end

function PipScrub:in_1_bang(sel)
    min_length = self.size / 100
    max_length = self.size - min_length
    length = math.random(min_length, max_length)
    offset = math.random(0, self.size - length)

    self:outlet(1, "list", { tostring(offset) })
end

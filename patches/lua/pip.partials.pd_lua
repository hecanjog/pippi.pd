local PipPartials = pd.Class:new():register("pip.partials")

function PipPartials:initialize(sel, atoms)
    self.inlets = 2
    self.outlets = 1
    
    self.partials = {}

    return true
end

function PipPartials:in_1_bang(sel, atoms)
    -- output message

    partialnum  = table.getn(self.partials)

    message = "sinesum 512"

    for p = 1, partialnum do
        partial = string.split(self.partials[p], ":")

        partial[2] = math.random() * partial[2]

        message = message .. " " .. partial[2]
    end

    self:outlet(1, "list", {message})
end

function PipPartials:in_2_list(sel, atoms)
    self.partials = string.split(atoms, " ")
end

function string:split(sep)
    local sep, fields = sep or ":", {}
    local pattern = string.format("([^%s]+)", sep)
    self:gsub(pattern, function(c) fields[#fields+1] = c end)
    return fields
end


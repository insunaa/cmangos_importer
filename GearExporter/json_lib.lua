-- Simple JSON serializer for WoW Lua (no nil values, no nested tables with mixed keys)

local currentIndent = 0

local function getIndent()
    return string.rep("  ", currentIndent)
end

local function jsonStringify(v)
    if type(v) == "table" then
        return toJson(v)
    elseif type(v) == "boolean" then
        return tostring(v)
    elseif type(v) == "number" then
        return tostring(v)
    elseif type(v) == "string" then
        v = string.gsub(v or "", "\\", "\\\\")
        v = string.gsub(v, '"', '\\"')
        v = string.gsub(v, "\n", "\\n")
        v = string.gsub(v, "\r", "\\r")
        v = string.gsub(v, "\t", "\\t")
        return string.format("%q", v)
    else
        return nil
    end
end

toJson = function(tbl, keyOrder)
    local out = {}
    local isArray = false
    local count = 0
    for k in pairs(tbl) do
        count = count + 1
        if type(k) == "number" then
            if k ~= count then
                return "{}"
            end
            if count == 1 then isArray = true end
        else
            isArray = false
        end
    end

    if count == 0 then
        return isArray and "[]" or "{}"
    end

    currentIndent = currentIndent + 1
    local innerParts = {}
    if isArray then
        for i = 1, count do
            local s = jsonStringify(tbl[i])
            if s ~= nil then
                table.insert(innerParts, getIndent() .. s)
            end
        end
    else
        local keys = keyOrder or nil
        if keys then
            for _, k in ipairs(keys) do
                local v = tbl[k]
                if v ~= nil then
                    local safeK = string.gsub(tostring(k), "\\", "\\\\")
                    safeK = string.gsub(safeK, '"', '\\"')
                    table.insert(innerParts, getIndent() .. '"' .. safeK .. '": ' .. jsonStringify(v))
                end
            end
        else
            for k, v in pairs(tbl) do
                if v ~= nil then
                    local safeK = string.gsub(tostring(k), "\\", "\\\\")
                    safeK = string.gsub(safeK, '"', '\\"')
                    table.insert(innerParts, getIndent() .. '"' .. safeK .. '": ' .. jsonStringify(v))
                end
            end
        end
    end
    currentIndent = currentIndent - 1

    local inner = table.concat(innerParts, ",\n")
    if isArray then
        return "[\n" .. inner .. "\n" .. getIndent() .. "]"
    else
        return "{\n" .. inner .. "\n" .. getIndent() .. "}"
    end
end

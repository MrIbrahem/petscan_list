local p = {}

local function fix_value(value, arg)
    value = mw.ustring.gsub(value, "%{%{%!%}%}", "|", 1)
    value = mw.ustring.gsub(value, "%{%{%|%}%}", "|", 1)
    if arg == "sparql" then
        return value
    end

    local splits = mw.text.split(value, "\n")
    -- if value has "\n" then split it by \n then join by \r\n
    -- mw.text.split

    if #splits > 1 then
        local values = {}
        for i, v in ipairs(splits) do
            v = mw.text.trim(v)
            v = mw.ustring.gsub(v, "^%s*%*%s*", "")
            table.insert(values, v)
            value = table.concat(values, "\r\n")
        end
    end
    return value
end

function p.url(frame)
    local args = frame:getParent().args
    local params = {}
    for arg, value in pairs(args) do
        -- if mw.ustring.find(tostring(value), "UNIQ--nowiki") then
        if string.find(tostring(value), "UNIQ--nowiki", 1, true) then
            value = mw.text.unstripNoWiki(value)
        end
        -- value = mw.text.unstripNoWiki(value)
        value = mw.text.killMarkers(value)
        value = mw.text.trim(value)
        arg = mw.text.trim(arg)

        -- if arg starts with _ ignore
        mw.log(arg, value)

        if arg:sub(1, 1) ~= "_" then
            value = fix_value(value, arg)
            if value ~= "" then
                value = mw.getCurrentFrame():callParserFunction('urlencode', value)
                arg = mw.getCurrentFrame():callParserFunction('urlencode', arg)
                table.insert(params, arg .. "=" .. value)
                -- mw.log(arg, value)
            end
        end
    end
    if params == 0 then
        return ""
    end
    local url = "https://petscan.wmcloud.org/?" .. table.concat(params, "&")
    -- local path_url = ("[%s %s]"):format(url, "PetScan")
    return url
end

return p

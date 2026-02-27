lyrics = {}
currentIndex = 1
lastKey = ""

function parseTimeToMs(timeStr)
    if not timeStr then return 0 end
    local min, sec = string.match(timeStr, "(%d+):(%d+)")
    if not min then return 0 end
    return (tonumber(min) * 60 + tonumber(sec)) * 1000
end

-- Normalize strings for loose matching
local function norm(s)
    if not s then return "" end
    s = s:lower()
    s = s:gsub("%b()", "")          -- remove ( ... )
    s = s:gsub("%b[]", "")          -- remove [ ... ]
    s = s:gsub("feat%.?", "")       -- remove feat/feat.
    s = s:gsub("ft%.?", "")         -- remove ft/ft.
    s = s:gsub("[^%w%s]", "")       -- remove punctuation
    s = s:gsub("%s+", " ")          -- collapse spaces
    return s:match("^%s*(.-)%s*$")  -- trim
end

-- Extract first non-null syncedLyrics string from LRCLIB /api/search JSON
function extractSyncedLyrics(json)
    if not json or json == "" then return nil end
    for s in string.gmatch(json, '"syncedLyrics"%s*:%s*"(.-)"') do
        if s and s ~= "" then
            return s
        end
    end
    return nil
end

-- Pull track/artist from LRCLIB JSON (first object)
function extractTrackArtist(json)
    local t = json:match('"trackName"%s*:%s*"(.-)"')
    local a = json:match('"artistName"%s*:%s*"(.-)"')
    return t, a
end

function Update()
    local title  = SKIN:GetMeasure("MeasureTitle"):GetStringValue() or ""
    local artist = SKIN:GetMeasure("MeasureArtist"):GetStringValue() or ""
    local posStr = SKIN:GetMeasure("MeasurePosition"):GetStringValue() or ""
    local json   = SKIN:GetMeasure("MeasureLyricsFetch"):GetStringValue() or ""

    if title == "" or artist == "" then return "" end

    local key = artist .. " — " .. title

    -- Track changed: clear lyrics and force a fetch
    if key ~= lastKey then
        lyrics = {}
        currentIndex = 1
        lastKey = key
        SKIN:Bang("!CommandMeasure", "MeasureLyricsFetch", "Run")
        return ""
    end

    if json == "" then return "" end

    -- Soft check (do NOT block display if mismatch)
    local jTitle, jArtist = extractTrackArtist(json)
    if jTitle and jArtist then
        local a1, t1 = norm(artist), norm(title)
        local a2, t2 = norm(jArtist), norm(jTitle)
        -- If it looks totally unrelated, wait for next fetch
        if (a2 ~= "" and a1 ~= "" and not string.find(a2, a1, 1, true) and not string.find(a1, a2, 1, true)) then
            return ""
        end
        if (t2 ~= "" and t1 ~= "" and not string.find(t2, t1, 1, true) and not string.find(t1, t2, 1, true)) then
            return ""
        end
    end

    local raw = extractSyncedLyrics(json)
    if not raw then
        lyrics = {}
        return ""
    end

    raw = raw:gsub("\\n", "\n")

    -- Parse once per track
    if #lyrics == 0 then
        for line in raw:gmatch("[^\r\n]+") do
            local time, text = line:match("%[(%d+:%d+%.?%d*)%](.*)")
            if time and text then
                local m, s = time:match("(%d+):(%d+%.?%d*)")
                local total = tonumber(m) * 60 + tonumber(s)
                table.insert(lyrics, { time = total * 1000, text = text })
            end
        end
    end

    -- Apply per-skin timing offset (ms). Positive shows later lines sooner (fixes "one line behind").
    local offset = tonumber(SKIN:GetVariable("LyricOffsetMs")) or 0
    local progress = parseTimeToMs(posStr) + offset
    if progress < 0 then progress = 0 end

    currentIndex = 1
    for i = 1, #lyrics do
        if progress >= lyrics[i].time then
            currentIndex = i
        else
            break
        end
    end

    return ""
end

function GetLine(offset)
    local idx = currentIndex + offset
    if lyrics[idx] then
        return lyrics[idx].text
    end
    return ""
end

-- Returns a font size for a given line (used to keep current lyrics from overflowing)
function GetSizeForLine(offset)
    local idx = currentIndex + offset
    local t = ""
    if lyrics[idx] and lyrics[idx].text then
        t = lyrics[idx].text
    end

    -- Base size comes from CurSize variable (defaults to 30 in your size preset)
    local base = tonumber(SKIN:GetVariable("CurSize")) or 30
    local len = #t

    -- Simple scaling tiers (tweak thresholds if you want)
    if len <= 34 then
        return base
    elseif len <= 55 then
        return math.max(base - 4, 18)   -- 26 if base=30
    elseif len <= 75 then
        return math.max(base - 8, 16)   -- 22 if base=30
    else
        return math.max(base - 10, 14)  -- 20 if base=30
    end
end
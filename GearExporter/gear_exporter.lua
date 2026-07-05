--------------------------------------------------------------------------------
-- Constants
--------------------------------------------------------------------------------

local VERSION             = "3.4"
local NUM_EQUIP_SLOTS     = 19
local NUM_ACTION_SLOTS    = 120
local NUM_MACRO_SLOTS     = 138

-- Mapping from WoW inventory slot index → human-readable key
local SLOT_NAMES          = {
    [1] = 'head',
    [2] = 'neck',
    [3] = 'shoulder',
    [4] = 'shirt',
    [5] = 'chest',
    [6] = 'waist',
    [7] = 'legs',
    [8] = 'feet',
    [9] = 'wrist',
    [10] = 'hands',
    [11] = 'finger1',
    [12] = 'finger2',
    [13] = 'trinket1',
    [14] = 'trinket2',
    [15] = 'back',
    [16] = 'main_hand',
    [17] = 'off_hand',
    [18] = 'relic',
    [19] = 'tabard',
    [20] = 'ammo',
    [21] = 'shield'
}

-- Equipment / off-hand item class IDs (weapon, armor)
local IS_EQUIPPABLE_CLASS = { [2] = true, [4] = true }

-- Max spell/quest IDs per expansion
local MAX_SPELL_IDS       = { [0] = 33400, [1] = 53100, [2] = 80900 }
local MAX_QUEST_IDS       = { [0] = 9665, [1] = 12515, [2] = 26034 }

--------------------------------------------------------------------------------
-- Helpers
--------------------------------------------------------------------------------

local function parseItemLink(itemLink)
    local itemString = string.match(itemLink, "item:([%-?%d:]+)")
    local result = {}
    for _, v in ipairs({ strsplit(":", itemString) }) do
        result[#result + 1] = (v == "") and 0 or tonumber(v)
    end
    return result
end

local function nilIfZero(val)
    return (val and val ~= 0) and val or nil
end

-- Extract gem list from parsed item link + collected socket colors.
-- Returns { {id, matched}, ... } or nil if no gems.
local function collectGems(itemSplit, gemColors)
    local gems = {}
    for idx = 1, 3 do
        local gemId = itemSplit[idx + 2] -- fields 3,4,5 are gem slots
        if gemId and gemId ~= 0 then
            table.insert(gems, { id = gemId, matched = gemColors[idx] })
        end
    end
    return #gems > 0 and gems or nil
end

-- Scan sockets on an item and collect gem colors + buckle flag.
-- caller must call C_ItemSocketInfo.CloseSocketInfo() after this returns.
local function scanSockets(itemLink, isEquipped, bag, slot)
    local hasBuckle = false
    local gemColors = { nil, nil, nil }

    if isEquipped then
        SocketInventoryItem(slot)
    else
        C_Container.SocketContainerItem(bag, slot)
    end

    for j = 1, C_ItemSocketInfo.GetNumSockets() do
        local equipLoc = select(9, C_Item.GetItemInfo(itemLink))
        if equipLoc == "INVTYPE_WAIST" then
            local sockType = C_ItemSocketInfo.GetSocketTypes(j)
            if sockType == "Prismatic" then
                hasBuckle = true
            end
        end
        _, _, gemColors[j] = C_ItemSocketInfo.GetExistingSocketInfo(j)
    end

    return hasBuckle, gemColors
end

-- Build an equipment/bag entry table from a parsed item link + socket info.
local function buildItemEntry(itemSplit)
    local suffix = -(itemSplit[7] or 0)
    if suffix == -0 then suffix = 0 end

    return {
        id        = itemSplit[1],
        suffix    = nilIfZero(suffix),
        unique    = nilIfZero(suffix) and bit.band(itemSplit[8], 65535) or nil,
        enchantId = nilIfZero(itemSplit[2]),
    }
end

--------------------------------------------------------------------------------
-- Data collectors (each returns a table fragment to merge into the root data)
--------------------------------------------------------------------------------

local function collectPlayerInfo()
    local _, rawClass = UnitClass("player")

    return {
        exporter_version = VERSION,
        player = {
            name        = GetUnitName("player"),
            class       = string.lower(rawClass),
            level       = UnitLevel("player"),
            race        = UnitRace("player"),
            gender      = UnitSex("player") - 2,
            region      = nil,
            server      = GetRealmName(),
            role        = "N/A",
            professions = "N/A",
            talents     = "N/A",
            spec        = "N/A",
            expansion   = GetExpansionLevel(),
            gold        = GetMoney(),
            locale      = GetLocale(),
        }
    }
end

local function collectEquipment()
    local equipment = {}

    for i = 1, NUM_EQUIP_SLOTS do
        local itemLink = GetInventoryItemLink("player", i)
        if itemLink then
            C_ItemSocketInfo.CloseSocketInfo()
            local split = parseItemLink(itemLink)

            -- Only store equippable items (class 2=armor, 4=weapon)
            local classID = select(12, C_Item.GetItemInfo(itemLink))
            if IS_EQUIPPABLE_CLASS[classID] then
                local hasBuckle, gemColors = scanSockets(itemLink, true, nil, i)
                C_ItemSocketInfo.CloseSocketInfo()

                local entry = buildItemEntry(split)
                entry.gems = collectGems(split, gemColors)
                if hasBuckle then entry.buckle = true end

                equipment[SLOT_NAMES[i]] = entry
            end
        end
    end

    C_ItemSocketInfo.CloseSocketInfo()

    return { equipment = equipment }
end

local function collectAmmo()
    local ammoId = GetInventoryItemID("player", 0)
    return ammoId and { ammo = { id = ammoId } } or {}
end

local function collectHunterData()
    if select(2, UnitClass("player")) ~= "HUNTER" then return {} end

    local result = {}
    local invId = C_Container.ContainerIDToInventoryID(4)
    local link = GetInventoryItemLink("player", invId)
    if link then
        result.quiver = { id = parseItemLink(link)[1] }
    end

    if UnitExists("pet") then
        local guid = UnitGUID("pet")
        local tokens = {}
        for token in string.gmatch(guid, "[^-]+") do
            tokens[#tokens + 1] = token
        end
        result.pet = {
            name   = UnitName("pet"),
            level  = UnitLevel("pet"),
            id     = tokens[6],
            family = UnitCreatureFamily("pet"),
            health = UnitHealthMax("pet"),
            power  = UnitPowerMax("pet"),
        }
    end

    return result
end

local function collectBagContents()
    local contents = {}

    -- Record equipped bag IDs
    for i = 1, 4 do
        local bagId = GetInventoryItemID("player", C_Container.ContainerIDToInventoryID(i))
        if bagId then
            table.insert(contents, { bag = i, id = bagId })
        end
    end

    -- Scan every container (0=backpack, 1-4=bags, 5+=bank)
    local maxBag = NUM_BAG_SLOTS + GetNumBankSlots()
    for bag = 0, maxBag do
        local numSlots = C_Container.GetContainerNumSlots(bag)
        for slot = 1, numSlots do
            local itemId = C_Container.GetContainerItemID(bag, slot)
            if itemId then
                local link = C_Container.GetContainerItemLink(bag, slot)
                local split = parseItemLink(link)

                local hasBuckle, gemColors = scanSockets(link, false, bag, slot)
                C_ItemSocketInfo.CloseSocketInfo()

                local entry = buildItemEntry(split)
                entry.bag   = bag
                entry.slot  = slot
                entry.count = C_Container.GetContainerItemInfo(bag, slot)["stackCount"]
                entry.gems  = collectGems(split, gemColors)
                if hasBuckle then entry.buckle = true end

                table.insert(contents, entry)
            end
        end
    end

    return { bagContents = contents }
end

local function collectActions()
    local actions = {}
    for i = 1, NUM_ACTION_SLOTS do
        local atype, id = GetActionInfo(i)
        if atype then
            table.insert(actions, { slot = i, type = atype, id = id })
        end
    end
    return { actions = actions }
end

local function collectMacros()
    local macros = {}
    for i = 1, NUM_MACRO_SLOTS do
        local name, icon, body, isLocal = GetMacroInfo(i)
        if name then
            table.insert(macros, {
                slot    = i,
                name    = name,
                texture = icon,
                body    = body,
                isLocal = isLocal,
            })
        end
    end
    return { macros = macros }
end

local function collectSpells()
    local spells = {}
    for i = 1, MAX_SPELL_IDS[GetExpansionLevel()] do
        if IsPlayerSpell(i) then
            table.insert(spells, i)
        end
    end
    return { spells = spells }
end

local function collectFactions()
    local factions = {}
    local idx = 1
    while idx <= GetNumFactions() do
        local name, _, _, _, _, earned, _, _,
        isHeader, isCollapsed, hasRep, _, _, factionId = GetFactionInfo(idx)

        if isHeader and isCollapsed then
            ExpandFactionHeader(idx)
        end

        if hasRep or not isHeader then
            table.insert(factions, {
                factionID   = factionId,
                name        = name,
                earnedValue = earned,
            })
        end

        idx = idx + 1
    end
    return { factions = factions }
end

local function collectQuests()
    local quests = {}
    for i = 1, MAX_QUEST_IDS[GetExpansionLevel()] do
        if C_QuestLog.IsQuestFlaggedCompleted(i) then
            table.insert(quests, i)
        end
    end
    return { quests = quests }
end

local function collectGlyphs()
    local expansion = GetExpansionLevel()
    if expansion ~= 2 then return {} end

    local glyphs = {}
    local group = GetActiveTalentGroup(false, false)
    for i = 1, GetNumGlyphSockets() do
        local spellId = select(3, GetGlyphSocketInfo(i, group))
        if spellId then
            table.insert(glyphs, { socket = i, spellID = spellId })
        end
    end
    return { glyphs = glyphs }
end

local function collectAchievements()
    local expansion = GetExpansionLevel()
    if expansion ~= 2 then return {} end

    local achievements = {}
    for _, catId in ipairs(GetCategoryList()) do
        if catId then
            local numAchievs = select(1, GetCategoryNumAchievements(catId))
            for i = 1, numAchievs do
                local id, _, _, completed, month, day, year = GetAchievementInfo(catId, i)
                if id and completed and year and month and day then
                    table.insert(achievements, {
                        id    = id,
                        year  = year,
                        month = month,
                        day   = day,
                    })
                end
            end
        end
    end
    return { achievements = achievements }
end

local function collectSkills()
    local skills = {}
    for i = 1, GetNumSkillLines() do
        local name, header, _, rank, _, _, maxRank = GetSkillLineInfo(i)
        if not header then
            table.insert(skills, { name = name, rank = rank, maxRank = maxRank })
        end
    end
    return { skills = skills }
end

--------------------------------------------------------------------------------
-- Merge a list of tables into one (shallow merge)
--------------------------------------------------------------------------------

local function mergeTables(...)
    local result = {}
    for _, tbl in ipairs({ ... }) do
        for k, v in pairs(tbl) do
            result[k] = v
        end
    end
    return result
end

--------------------------------------------------------------------------------
-- Public API
--------------------------------------------------------------------------------

function scanGear()
    QEProfile = ""

    local data = mergeTables(
        collectPlayerInfo(),
        collectEquipment(),
        collectAmmo(),
        collectHunterData(),
        collectBagContents(),
        collectActions(),
        collectMacros(),
        collectSpells(),
        collectFactions(),
        collectQuests(),
        collectGlyphs(),
        collectAchievements(),
        collectSkills()
    )

    local rootKeys = {
        "exporter_version", "player", "equipment", "ammo", "quiver", "pet",
        "bagContents", "actions", "macros", "spells", "factions",
        "quests", "glyphs", "achievements", "skills"
    }
    QEProfile = toJson(data, rootKeys)
    GetMainFrame(QEProfile):Show()
end

function GetMainFrame(text)
    if SimcFrame then
        SimcEditBox:SetText(text)
        SimcEditBox:HighlightText()
        return SimcFrame
    end

    local frameW, frameH = 750, 400

    -- Base frame with built-in title bar and backdrop
    local f = CreateFrame("Frame", "SimcFrame", UIParent, "DialogBoxFrame")
    f:ClearAllPoints()
    f:SetPoint("CENTER")
    f:SetSize(frameW, frameH)
    f:SetMovable(true)
    f:SetClampedToScreen(true)

    -- Make the title bar draggable.  The DialogBoxFrame template creates a title
    -- texture at roughly y=-15..-37 from the frame top; we overlay an invisible
    -- hitbox there so dragging works without stealing clicks from children.
    local dragBar = CreateFrame("Button", nil, f)
    dragBar:SetPoint("TOPLEFT", 14, -15)
    dragBar:SetPoint("TOPRIGHT", -14, -15)
    dragBar:SetHeight(22)
    dragBar:RegisterForClicks("LeftButtonUp")
    dragBar:SetScript("OnMouseDown", function(self, btn)
        if btn == "LeftButton" then f:StartMoving() end
    end)
    dragBar:SetScript("OnMouseUp", function()
        f:StopMovingOrSizing()
    end)

    -- Scrollable text area
    local sf = CreateFrame("ScrollFrame", "SimcScrollFrame", f, "UIPanelScrollFrameTemplate")
    sf:SetPoint("TOPLEFT", 16, -34)
    sf:SetPoint("BOTTOMRIGHT", f, "BOTTOMRIGHT", -28, 45)

    local eb = CreateFrame("EditBox", "SimcEditBox", sf)
    eb:SetMultiLine(true)
    eb:SetAutoFocus(true)
    eb:SetFontObject("ChatFontNormal")
    eb:SetMaxLetters(0)
    eb:SetTextInsets(4, 4, 4, 4)
    eb:SetScript("OnEscapePressed", function() f:Hide() end)
    sf:SetScrollChild(eb)

    -- Resize handle in the bottom-right corner
    f:SetResizable(true)
    local rb = CreateFrame("Button", nil, f)
    rb:SetPoint("BOTTOMRIGHT", -6, 7)
    rb:SetSize(16, 16)
    rb:SetNormalTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Up")
    rb:SetHighlightTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Highlight")
    rb:SetPushedTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Down")
    rb:RegisterForClicks("LeftButtonUp")
    rb:SetScript("OnMouseDown", function(self, btn)
        if btn == "LeftButton" then
            f:StartSizing("BOTTOMRIGHT")
            self:GetHighlightTexture():Hide()
        end
    end)
    rb:SetScript("OnMouseUp", function(self)
        f:StopMovingOrSizing()
        self:GetHighlightTexture():Show()
        eb:SetWidth(sf:GetWidth() - 16) -- account for scrollbar width
    end)

    -- On frame resize, keep the editbox width correct.
    f:SetScript("OnSizeChanged", function()
        eb:SetWidth(sf:GetWidth() - 16)
    end)

    SimcFrame = f
    SimcEditBox:SetText(text)
    SimcEditBox:HighlightText()
    return f
end

SLASH_GEAREXPORT1 = "/gearexport";
SlashCmdList["GEAREXPORT"] = scanGear;

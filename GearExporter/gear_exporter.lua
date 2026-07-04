qeVersionNum = "3.3"
QEProfile = ""

local function GetItemSplit(itemLink)
    local itemString = string.match(itemLink, "item:([%-?%d:]+)")
    local itemSplit = {}

    for _, v in ipairs({ strsplit(":", itemString) }) do
        if v == "" then
            itemSplit[#itemSplit + 1] = 0
        else
            itemSplit[#itemSplit + 1] = tonumber(v)
        end
    end

    return itemSplit
end

-- Helper: build an item record table from the raw data extracted by GetItemSplit / socket API
local function toItemRecord(itemID, suffix, enchantId, gem1, gem2, gem3, gemColors, hasBuckle, count)
    local record = { id = itemID }
    if suffix and suffix ~= 0 then
        record.suffix = suffix
    end
    if enchantId and enchantId ~= 0 then
        record.enchantId = enchantId
    end
    -- Gems are always present but may be nil / 0
    if gem1 and gem1 ~= 0 then
        record.gems = { tostring(gem1) .. ":" .. (gemColors[1] or "nil") }
        if gem2 and gem2 ~= 0 then
            table.insert(record.gems, tostring(gem2) .. ":" .. (gemColors[2] or "nil"))
        end
        if gem3 and gem3 ~= 0 then
            table.insert(record.gems, tostring(gem3) .. ":" .. (gemColors[3] or "nil"))
        end
    end
    if hasBuckle == true then
        record.buckle = true
    end
    if count then
        record.count = count
    end
    return record
end

local function getSockets(equipID, itemLink)
    -- Returns { enchantId, gem1, gem2, gem3, { color1, color2, color3 }, hasBuckle }
    local enchantId = 0
    local gem1, gem2, gem3 = 0, 0, 0
    local gemColors = { nil, nil, nil }
    local hasBuckle = false

    SocketInventoryItem(0) -- placeholder; real code uses inventory bag/slot below
    CloseSocketInfo()

    -- We rely on caller passing itemSplit already; this is a convenience for non-equip items
    return enchantId, gem1, gem2, gem3, gemColors, hasBuckle
end

function scanGear()
    QEProfile = ""

    local slotNames = {
        'head',      -- [1]
        'neck',      -- [2]
        'shoulder',  -- [3]
        'shirt',     -- [6]
        'chest',     -- [5]
        'waist',     -- [10]
        'legs',      -- [11]
        'feet',      -- [12]
        'wrist',     -- [8]
        'hands',     -- [9]
        'finger1',   -- [13]
        'finger2',   -- [14]
        'trinket1',  -- [15]
        'trinket2',  -- [16]
        'back',      -- [4]
        'main_hand', -- [17]
        'off_hand',  -- [18]
        'relic',     -- [18]

        'tabard',    -- [7]
        'ammo',      -- [19]
        'shield'     -- [20]
    }

    local pName = GetUnitName("player")
    local _, pClass, _ = UnitClass("player")
    pClass = string.lower(pClass)
    local expansion = GetExpansionLevel()

    -- ===== Build the structured root table =====
    local data = {}

    -- Top-level metadata
    data.exporter_version = qeVersionNum

    -- Player identity
    data.player = {
        name        = pName,
        class       = pClass,
        level       = UnitLevel("player"),
        race        = UnitRace("player"),
        gender      = UnitSex("player") - 2,
        region      = nil, -- not available via API in classic
        server      = GetRealmName(),
        role        = "N/A",
        professions = "N/A",
        talents     = "N/A",
        spec        = "N/A",
        expansion   = expansion,
        gold        = GetMoney(),
        locale      = GetLocale()
    }

    -- Equipped items (slots 1-19)
    data.equipment = {}
    for i = 1, 19, 1 do
        local equipID = GetInventoryItemID("player", i)
        local itemLink = GetInventoryItemLink('player', i)

        if equipID ~= nil then
            local itemSplit = GetItemSplit(itemLink)
            local suffix = itemSplit[7] * -1
            if suffix == -0 then suffix = 0 end
            local enchantId = itemSplit[2]
            local gem1, gem2, gem3 = itemSplit[3], itemSplit[4], itemSplit[5]

            -- Socket info
            local equipLoc
            local hasBuckle = false
            local gemColors = { nil, nil, nil }
            SocketInventoryItem(i)
            for j = 1, GetNumSockets() do
                _, _, _, _, _, _, _, _, equipLoc = GetItemInfo(itemLink)
                if equipLoc ~= nil and equipLoc == "INVTYPE_WAIST" then
                    if GetSocketTypes(j) ~= nil and GetSocketTypes(j) == "Prismatic" then
                        hasBuckle = true
                    end
                end
                _, _, gemColors[j] = GetExistingSocketInfo(j)
            end
            CloseSocketInfo()

            local _, _, _, _, _, _, _,
            _, itemEquipLoc, _, _, classID, subclassID = GetItemInfo(itemLink)

            if classID == 2 or classID == 4 then
                -- Store under the slot name key — same structure as bag items
                data.equipment[slotNames[i]] = {
                    slot      = slotNames[i],
                    id        = equipID,
                    suffix    = (suffix and suffix ~= 0) and suffix or nil,
                    unique    = (suffix and suffix ~= 0) and bit.band(itemSplit[8], 65535) or nil,
                    enchantId = (enchantId and enchantId ~= 0) and enchantId or nil,
                }

                -- Gems array (only include non-zero gems)
                local gemArray = {}
                if gem1 and gem1 ~= 0 then
                    table.insert(gemArray,
                        tostring(gem1) .. ":" .. tostring(gemColors[1] or "nil"))
                end
                if gem2 and gem2 ~= 0 then
                    table.insert(gemArray,
                        tostring(gem2) .. ":" .. tostring(gemColors[2] or "nil"))
                end
                if gem3 and gem3 ~= 0 then
                    table.insert(gemArray,
                        tostring(gem3) .. ":" .. tostring(gemColors[3] or "nil"))
                end
                if #gemArray > 0 then
                    data.equipment[slotNames[i]].gems = gemArray
                end
                if hasBuckle then
                    data.equipment[slotNames[i]].buckle = true
                end
            end
        end
    end

    -- Ammo (slot 0)
    local ammoID = GetInventoryItemID("player", 0)
    if ammoID ~= nil then
        data.ammo = { id = ammoID }
    end

    -- Hunter quiver + pet
    if pClass == "hunter" then
        local invID = C_Container.ContainerIDToInventoryID(4)
        local bagLink = GetInventoryItemLink("player", invID)
        local bagSplit = GetItemSplit(bagLink)
        data.quiver = { id = bagSplit[1] }

        if UnitExists("pet") then
            local petID = UnitGUID("pet")
            local tokens = {}
            local idx = 1
            for token in string.gmatch(petID, "[^-]+") do
                tokens[idx] = token
                idx = idx + 1
            end
            data.pet = {
                name   = UnitName("pet"),
                level  = UnitLevel("pet"),
                id     = tokens[6],
                family = UnitCreatureFamily("pet"),
                health = UnitHealthMax("pet"),
                power  = UnitPowerMax("pet")
            }
        end
    end

    -- Bag items (equipped bags 1-4, then all bag slots)
    data.bagContents = {}

    -- Quick list of equipped bags
    for i = 1, 4, 1 do
        local equipID = GetInventoryItemID("player", C_Container.ContainerIDToInventoryID(i))
        if equipID ~= nil then
            table.insert(data.bagContents, { bag = i, id = equipID })
        end
    end

    -- All items across all bags (0 = backpack, 1-4 = bags, 5+ = bank)
    for bag = 0, (NUM_BAG_SLOTS + GetNumBankSlots()) do
        if C_Container.GetContainerNumSlots(bag) ~= 0 then
            for bagSlot = 1, C_Container.GetContainerNumSlots(bag) do
                local itemID = C_Container.GetContainerItemID(bag, bagSlot)

                if itemID then
                    local itemLink = C_Container.GetContainerItemLink(bag, bagSlot)
                    local itemSplit = GetItemSplit(itemLink)
                    local suffix = itemSplit[7] * -1
                    if suffix == -0 then suffix = 0 end
                    local enchantId = itemSplit[2]
                    local gem1, gem2, gem3 = itemSplit[3], itemSplit[4], itemSplit[5]

                    local hasBuckle = false
                    local gemColors = { nil, nil, nil }

                    C_Container.SocketContainerItem(bag, bagSlot)
                    for j = 1, GetNumSockets() do
                        local equipLoc
                        _, _, _, _, _, _, _, _, equipLoc = GetItemInfo(itemLink)
                        if equipLoc ~= nil and equipLoc == "INVTYPE_WAIST" then
                            if GetSocketTypes(j) ~= nil and GetSocketTypes(j) == "Prismatic" then
                                hasBuckle = true
                            end
                        end
                        _, _, gemColors[j] = GetExistingSocketInfo(j)
                    end
                    CloseSocketInfo()

                    local itemCount = C_Container.GetContainerItemInfo(bag, bagSlot)["stackCount"]

                    table.insert(data.bagContents, {
                        bag       = bag,
                        slot      = bagSlot,
                        id        = itemID,
                        suffix    = (suffix and suffix ~= 0) and suffix or nil,
                        unique    = (suffix and suffix ~= 0) and bit.band(itemSplit[8], 65535) or nil,
                        count     = itemCount,
                        enchantId = (enchantId and enchantId ~= 0) and enchantId or nil,
                        gems      = nil, -- populated below
                    })

                    -- Gems
                    local gemArray = {}
                    if gem1 and gem1 ~= 0 then
                        table.insert(gemArray,
                            tostring(gem1) .. ":" .. tostring(gemColors[1] or "nil"))
                    end
                    if gem2 and gem2 ~= 0 then
                        table.insert(gemArray,
                            tostring(gem2) .. ":" .. tostring(gemColors[2] or "nil"))
                    end
                    if gem3 and gem3 ~= 0 then
                        table.insert(gemArray,
                            tostring(gem3) .. ":" .. tostring(gemColors[3] or "nil"))
                    end
                    if #gemArray > 0 then
                        data.bagContents[#data.bagContents].gems = gemArray
                    end
                    if hasBuckle then
                        data.bagContents[#data.bagContents].buckle = true
                    end
                end
            end
        end
    end

    -- Talents
    data.talents = {}
    local numTabs = 3
    for t = 1, numTabs do
        local numTalents = GetNumTalents(t)
        for i = 1, numTalents do
            local nameTalent, icon, tier, column, currRank, maxRank = GetTalentInfo(t, i)
            table.insert(data.talents, {
                talentGroup = t,
                id          = i,
                rank        = currRank
            })
        end
    end

    -- Action bar bindings
    data.actions = {}
    for i = 1, 120 do
        local atype, id = GetActionInfo(i)
        if atype ~= nil then
            table.insert(data.actions, {
                slot = i,
                type = atype,
                id   = id
            })
        end
    end

    -- Macros
    data.macros = {}
    local numMacros = 138
    for t = 1, numMacros do
        local name, iconTexture, body, isLocal = GetMacroInfo(t)
        if name ~= nil then
            table.insert(data.macros, {
                slot    = t,
                name    = name,
                texture = iconTexture,
                body    = body,
                isLocal = isLocal
            })
        end
    end

    -- Spells
    data.spells = {}
    local maxSpells = 33400
    if expansion == 1 then maxSpells = 53100 end
    if expansion == 2 then maxSpells = 80900 end
    for i = 1, maxSpells do
        if IsPlayerSpell(i) then
            table.insert(data.spells, i)
        end
    end

    -- Factions (reputation)
    data.factions = {}
    local numFactions = GetNumFactions()
    local factionIndex = 1
    while factionIndex <= numFactions do
        local name, description, standingId, bottomValue, topValue, earnedValue, atWarWith, canToggleAtWar,
        isHeader, isCollapsed, hasRep, isWatched, isChild, factionID, hasBonusRepGain, canBeLFGBonus = GetFactionInfo(
            factionIndex)
        if isHeader and isCollapsed then
            ExpandFactionHeader(factionIndex)
            numFactions = GetNumFactions()
        end
        if hasRep or not isHeader then
            table.insert(data.factions, {
                factionID   = factionID,
                name        = name,
                earnedValue = earnedValue
            })
        end
        factionIndex = factionIndex + 1
    end

    -- Quests
    data.quests = {}
    local maxQuests = 9665
    if expansion == 1 then maxQuests = 12515 end
    if expansion == 2 then maxQuests = 26034 end
    for i = 1, maxQuests do
        if C_QuestLog.IsQuestFlaggedCompleted(i) then
            table.insert(data.quests, i)
        end
    end

    -- Glyphs
    data.glyphs = {}
    if expansion == 2 then
        local glyphIndex = 1
        while glyphIndex <= GetNumGlyphSockets() do
            local talentGroup = GetActiveTalentGroup(false, false)
            local _, _, glyphSpellID, _ = GetGlyphSocketInfo(glyphIndex, talentGroup)
            if glyphSpellID ~= nil then
                table.insert(data.glyphs, {
                    socket  = glyphIndex,
                    spellID = glyphSpellID
                })
            end
            glyphIndex = glyphIndex + 1
        end
    end

    -- Achievements
    data.achievements = {}
    if expansion == 2 then
        local categories = GetCategoryList()
        for _, catId in ipairs(categories) do
            if catId ~= nil then
                local achievementId = 1
                local numAchievs, _, _ = GetCategoryNumAchievements(catId)
                while achievementId <= numAchievs do
                    local id, _, _, completed, month, day, year = GetAchievementInfo(catId, achievementId)
                    -- (extra trailing vars collapsed — original had 16 capture groups)
                    if id ~= nil and completed ~= nil and year ~= nil and month ~= nil and day ~= nil then
                        table.insert(data.achievements, {
                            id    = id,
                            year  = year,
                            month = month,
                            day   = day
                        })
                    end
                    achievementId = achievementId + 1
                end
            end
        end
    end

    -- Skills
    data.skills = {}
    for i = 1, GetNumSkillLines() do
        local skillName, header, _, skillRank, _, _, skillMaxRank = GetSkillLineInfo(i)
        if header == nil then
            table.insert(data.skills, {
                name    = skillName,
                rank    = skillRank,
                maxRank = skillMaxRank
            })
        end
    end

    -- ===== Serialize to JSON and display =====
    QEProfile = toJson(data)
    local f = GetMainFrame(QEProfile)
    f:Show()
end

function GetMainFrame(text)
    if not SimcFrame then
        frameConfig = {
            point         = "CENTER",
            relativeFrame = nil,
            relativePoint = "CENTER",
            ofsx          = 0,
            ofsy          = 0,
            width         = 750,
            height        = 400,
        }
        local f = CreateFrame("Frame", "SimcFrame", UIParent, "DialogBoxFrame")
        f:ClearAllPoints()
        f:SetPoint(
            frameConfig.point,
            frameConfig.relativeFrame,
            frameConfig.relativePoint,
            frameConfig.ofsx,
            frameConfig.ofsy
        )
        f:SetSize(frameConfig.width, frameConfig.height)
        f:SetBackdrop({
            bgFile   = "Interface\\DialogFrame\\UI-DialogBox-Background",
            edgeFile = "Interface\\PVPFrame\\UI-Character-PVP-Highlight",
            edgeSize = 16,
            insets   = { left = 8, right = 8, top = 8, bottom = 8 },
        })
        f:SetMovable(true)
        f:SetClampedToScreen(true)
        f:SetScript("OnMouseDown", function(self, button)
            if button == "LeftButton" then
                self:StartMoving()
            end
        end)
        f:SetScript("OnMouseUp", function(self, button)
            self:StopMovingOrSizing()
            point, relativeFrame, relativeTo, ofsx, ofsy = self:GetPoint()
            frameConfig.point                            = point
            frameConfig.relativeFrame                    = relativeFrame
            frameConfig.relativePoint                    = relativeTo
            frameConfig.ofsx                             = ofsx
            frameConfig.ofsy                             = ofsy
        end)

        local closeBtn = CreateFrame("Button", "SimcCloseButton", f, "UIPanelButtonTemplate")
        closeBtn:SetText("Copy")
        closeBtn:SetWidth(100)
        closeBtn:SetHeight(25)
        closeBtn:SetPoint("BOTTOM", f, "BOTTOM", 0, 15)
        closeBtn:SetScript("OnClick", function()
            SetClipboardText(SimcEditBox:GetText())
            f:Hide()
        end)

        local sf = CreateFrame("ScrollFrame", "SimcScrollFrame", f, "UIPanelScrollFrameTemplate")
        sf:SetPoint("LEFT", 16, 0)
        sf:SetPoint("RIGHT", -16, 0)
        sf:SetPoint("TOP", 0, -32)
        sf:SetPoint("BOTTOM", closeBtn, "TOP", 0, -10)

        local eb = CreateFrame("EditBox", "SimcEditBox", SimcScrollFrame)
        eb:SetSize(sf:GetSize())
        eb:SetMultiLine(true)
        eb:SetAutoFocus(true)
        eb:SetFontObject("ChatFontNormal")
        eb:SetScript("OnEscapePressed", function() f:Hide() end)
        sf:SetScrollChild(eb)

        f:SetResizable(true)
        local rb = CreateFrame("Button", "SimcResizeButton", f)
        rb:SetPoint("BOTTOMRIGHT", -6, 7)
        rb:SetSize(16, 16)
        rb:SetNormalTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Up")
        rb:SetHighlightTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Highlight")
        rb:SetPushedTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Down")
        rb:SetScript("OnMouseDown", function(self, button)
            if button == "LeftButton" then
                f:StartSizing("BOTTOMRIGHT")
                self:GetHighlightTexture():Hide()
            end
        end)
        rb:SetScript("OnMouseUp", function(self, button)
            f:StopMovingOrSizing()
            self:GetHighlightTexture():Show()
            eb:SetWidth(sf:GetWidth())
            frameConfig.width  = f:GetWidth()
            frameConfig.height = f:GetHeight()
        end)

        SimcFrame = f
    end
    SimcEditBox:SetText(text)
    SimcEditBox:HighlightText()
    return SimcFrame
end

function convertSlot(raw)
    if raw == "INVTYPE_HEAD" then
        return "head"
    elseif raw == "INVTYPE_NECK" then
        return "neck"
    elseif raw == "INVTYPE_SHOULDER" then
        return "shoulder"
    elseif raw == "INVTYPE_CHEST" then
        return "chest"
    elseif raw == "INVTYPE_WAIST" then
        return "waist"
    elseif raw == "INVTYPE_LEGS" then
        return "legs"
    elseif raw == "INVTYPE_FEET" then
        return "feet"
    elseif raw == "INVTYPE_WRIST" then
        return "wrist"
    elseif raw == "INVTYPE_HAND" then
        return "hand"
    elseif raw == "INVTYPE_FINGER" then
        return "finger1"
    elseif raw == "INVTYPE_CLOAK" then
        return "back"
    elseif raw == "INVTYPE_WEAPON" then
        return "one_hand"
    elseif raw == "INVTYPE_SHIELD" then
        return "shield"
    elseif raw == "INVTYPE_2HWEAPON" then
        return "main_hand"
    elseif raw == "INVTYPE_WEAPONMAINHAND" then
        return "main_hand"
    elseif raw == "INVTYPE_WEAPONOFFHAND" then
        return "off_hand"
    elseif raw == "INVTYPE_TRINKET" then
        return "trinket1"
    elseif raw == "INVTYPE_RELIC" then
        return "relic"
    else
        return "unknown"
    end
end

SLASH_GEAREXPORT1 = "/gearexport";
SlashCmdList["GEAREXPORT"] = scanGear;

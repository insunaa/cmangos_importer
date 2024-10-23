qeVersionNum = "1.3"
QEProfile = ""

local function GetItemSplit(itemLink)
  local itemString = string.match(itemLink, "item:([%-?%d:]+)")
  local itemSplit = {}

  -- Split data into a table
  for _, v in ipairs({strsplit(":", itemString)}) do
    if v == "" then
      itemSplit[#itemSplit + 1] = 0
    else
      itemSplit[#itemSplit + 1] = tonumber(v)
    end
  end

  return itemSplit
end

function scanGear() 
	QEProfile = "" -- Reset text.
	
	slotNames = {
	'head', -- [1]
	'neck', -- [2]
	'shoulder', -- [3]
	'shirt', -- [6]
	'chest', -- [5]
	'waist', -- [10]
	'legs', -- [11]
	'feet', -- [12]
	'wrist', -- [8]
	'hands', -- [9]
	'finger1', -- [13]
	'finger2', -- [14]
	'trinket1', -- [15]
	'trinket2', -- [16]
	'back', -- [4]
	'main_hand', -- [17]
	'off_hand', -- [18]
	'relic', -- [18]
	
	'tabard', -- [7]
	'ammo', -- [19]
	'shield' -- [20]
	}
	
	
	pname = GetUnitName("player")
	_, pclass, _ = 	UnitClass("player")
	pclass = string.lower(pclass)

	addPrint("QE Live Gear Importer v" .. qeVersionNum)
	addPrint("questionablyepic.com/live - Addon based heavily on SimulationCraft")
	addPrint(" ")
	addPrint(pclass .. '="' .. pname .. '"')
	addPrint("level=" .. UnitLevel("player"))
	addPrint("race=" .. UnitRace("player"))
	addPrint("gender=" .. UnitSex("player") - 2)
	addPrint("region=")
	addPrint("server=" .. GetRealmName())
	addPrint("role=N/A")
	addPrint("professions=N/A")
	addPrint("talents=N/A")
	addPrint("spec=N/A")
	addPrint("expansion=" .. GetExpansionLevel())
	addPrint("gold=" .. GetMoney())
	addPrint(" ")
	
	-- for loop for equipment
	
	for i=1, 19, 1  do
		local equipID = GetInventoryItemID("player", i);
		local itemLink = GetInventoryItemLink('player', i)

		if (equipID ~= nil) then
			local itemSplit = GetItemSplit(itemLink)
			local suffix = itemSplit[7] * -1
			if (suffix ~= -0) then
				local unique = bit.band(itemSplit[8], 65535)
				suffix = ",suffix=" .. suffix .. ",unique=" .. unique
			else suffix = "" end
			local hasBuckle = false
			--local _, enchantId, gem1, gem2, gem3, gem4 = string.match(itemLink, "item:(%d+):(%d+):(%d+):(%d+):(%d+):(%d+)")
			local enchantId = itemSplit[2]
			local gem1 = itemSplit[3]
			local gem2 = itemSplit[4]
			local gem3 = itemSplit[5]
			SocketInventoryItem(i)
			gemColors = {nil, nil, nil}
			for j=1, GetNumSockets() do
				_, _, _, _, _, _, _, _, equipLoc = GetItemInfo(itemLink)
				if (equipLoc ~= nil and equipLoc == "INVTYPE_WAIST") then
					if (GetSocketTypes(j) ~= nil and GetSocketTypes(j) == "Prismatic") then
						hasBuckle = true
					end
				end
				_, _, gemColors[j] = GetExistingSocketInfo(j)
			end
			CloseSocketInfo()
			local itemName, _, _, _, _, _, _, _, _, _, _, classID, subclassID = GetItemInfo(equipID);
			if (classID == 2 or classID == 4) then
				addPrint(slotNames[i] .. "=,id=" .. equipID .. suffix .. ",enchantId=" .. enchantId .. ",gem1=" .. gem1 ..":" .. tostring(gemColors[1]) .. ",gem2=" .. gem2 ..":" .. tostring(gemColors[2]) .. ",gem3=" .. gem3 ..":" .. tostring(gemColors[3]) .. ",buckle=" .. tostring(hasBuckle))
			end
		end
		
	end
	
	local ammoID = GetInventoryItemID("player", 0);
	if (ammoID ~= nil) then
		addPrint("ammo=,id=" .. ammoID)
	end
	if (pclass == "hunter") then
		local invID = C_Container.ContainerIDToInventoryID(4)
		local bagLink = GetInventoryItemLink("player", invID)
		local bagSplit = GetItemSplit(bagLink)
		addPrint("quiver=,id=" .. bagSplit[1])
		if (UnitExists("pet") ~= nil) then
			petID = UnitGUID("pet")
			i = 1
			local tokens = {}
			for token in string.gmatch(petID, "[^-]+") do
				tokens[i] = token
				i = i+1
			end
			addPrint("")
			addPrint("pet=" .. UnitName("pet") .. ",lv=" .. UnitLevel("pet") .. ",id=" .. tokens[6] .. ",family=" .. UnitCreatureFamily("pet") .. ",health=" .. UnitHealthMax("pet") .. ",power=" .. UnitPowerMax("pet"))
		end
	end

	addPrint("")
	addPrint("### GEAR FROM BAGS ###")

	if (true) then
		--for i=20, 23, 1  do
		for i=1, 4, 1 do
			local equipID = GetInventoryItemID("player", C_Container.ContainerIDToInventoryID(i));
			if equipID ~= nil then
				addPrint(i .. "," .. equipID)
			end
		end
	end

	for bag=0, (NUM_BAG_SLOTS + GetNumBankSlots()) do
		if (C_Container.GetContainerNumSlots(bag) ~= 0) then
			for bagSlots=1, C_Container.GetContainerNumSlots(bag) do
				local itemID = C_Container.GetContainerItemID(bag, bagSlots);
				
				if (itemID) then 
					local itemName, _, itemRarity, itemLevel, itemMinLevel, itemType, itemSubType, itemStackCount, itemEquipLoc, itemTexture, vendorPrice, classID, subclassID = GetItemInfo(itemID);
					
					local itemLink = C_Container.GetContainerItemLink(bag, bagSlots)
					local itemSplit = GetItemSplit(itemLink)
					local suffix = itemSplit[7] * -1
					local hasBuckle = false
					local enchantId = itemSplit[2]
					local gem1 = itemSplit[3]
					local gem2 = itemSplit[4]
					local gem3 = itemSplit[5]
					
					if (suffix ~= -0) then
						local unique = bit.band(itemSplit[8], 65535)
						suffix = ",suffix=" .. suffix .. ",unique=" .. unique
					else suffix = "" end
					
					C_Container.SocketContainerItem(bag, bagSlots)
					gemColors = {nil, nil, nil}
					for j=1, GetNumSockets() do
						_, _, _, _, _, _, _, _, equipLoc = GetItemInfo(itemLink)
						if (equipLoc ~= nil and equipLoc == "INVTYPE_WAIST") then
							if (GetSocketTypes(j) ~= nil and GetSocketTypes(j) == "Prismatic") then
								hasBuckle = true
							end
						end
						_, _, gemColors[j] = GetExistingSocketInfo(j)
					end
					CloseSocketInfo()
					
					local itemCount = C_Container.GetContainerItemInfo(bag, bagSlots)["stackCount"]
					addPrint("bag=" .. bag .. ",slot=" .. bagSlots ..",id=" .. itemID .. suffix .. ",count=" .. itemCount .. ",enchantId=" .. enchantId .. ",gem1=" .. gem1 ..":" .. tostring(gemColors[1]) .. ",gem2=" .. gem2 ..":" .. tostring(gemColors[2]) .. ",gem3=" .. gem3 ..":" .. tostring(gemColors[3]) .. ",buckle=" .. tostring(hasBuckle))
				end
			end
		end
	end

	addPrint("")
	addPrint("### TALENTS ###")

	local numTabs = 3;
	for t=1, numTabs do
		local numTalents = GetNumTalents(t);
		for i=1, numTalents do
			nameTalent, icon, tier, column, currRank, maxRank = GetTalentInfo(t,i);
			addPrint("t="..t..",id="..i..",rank="..currRank);
		end
	end

	addPrint("")
	addPrint("### ACTIONS ###")
	for i = 1, 120 do
		local type, id = GetActionInfo(i)
		if (type ~= nil) then
			addPrint("slot=" .. i .. ",type=" .. type .. ",id=" .. id)
		end	
	end

	addPrint("")
	addPrint("### MACROS ###")
	local numMacros = 138
	for t=1, numMacros do
		local name, iconTexture, body, isLocal = GetMacroInfo(t);
		if (name ~= nil) then
			addPrint("slot="..t..",name="..string.gsub(name, ",", ".")..",texture="..iconTexture..",body=")
			addPrint("---")
			addPrint(string.gsub(body, ",", "."))
			addPrint("---")
		end
	end

	addPrint("")
	addPrint("### SPELLS ###")

	local maxSpells = 33400

	if (expansion == 1) then
		maxSpells = 53100
	if (expansion == 2) then
		maxSpells = 80900

	for i = 1, maxSpells do
		if (IsPlayerSpell(i)) then
			addPrint(i)
		end
	end

	addPrint("")
	addPrint("### FACTIONS ###")

	local numFactions = GetNumFactions()
	local factionIndex = 1
	while (factionIndex <= numFactions) do
		local name, description, standingId, bottomValue, topValue, earnedValue, atWarWith, canToggleAtWar,
			isHeader, isCollapsed, hasRep, isWatched, isChild, factionID, hasBonusRepGain, canBeLFGBonus = GetFactionInfo(factionIndex)
		if isHeader and isCollapsed then
			ExpandFactionHeader(factionIndex)
			numFactions = GetNumFactions()
		end
		if hasRep or not isHeader then
			addPrint(factionID .. "," ..earnedValue)
		end
		factionIndex = factionIndex + 1
	end

	local expansion = GetExpansionLevel()

	if (expansion == 2) then
		addPrint("")
		addPrint("### GLYPHS ###")

		local glyphIndex = 1
		while (glyphIndex <= GetNumGlyphSockets()) do
			local talentGroup = GetActiveTalentGroup(false, false)
			local _, _, glyphSpellID, _ = GetGlyphSocketInfo(glyphIndex, talentGroup)
			if (glyphSpellID ~= nil) then
				addPrint(glyphIndex .. "," .. glyphSpellID)
			end
			glyphIndex = glyphIndex + 1
		end

		addPrint("")
		addPrint("### ACHIEVEMENTS ###")

		local categories = GetCategoryList()
		
		for k,j in ipairs(categories) do
			if (j ~= nil) then
				local achievementId = 1
				local numAchievs, _, _ = GetCategoryNumAchievements(j)
				while (achievementId <= numAchievs) do
					local id, _, _, completed, month, day, year, _, _, _, _, _, _, _, _ = GetAchievementInfo(j, achievementId)
					if (id ~= nil and completed ~= nil and year ~= nil and month ~=nil and day ~= nil) then
						addPrint(id .. "," .. year .. "," .. month .. "," .. day)
					end
					achievementId = achievementId + 1
				end
			end
		end
	else
		addPrint("")
		addPrint("### GLYPHS ###")
		addPrint("")
		addPrint("### ACHIEVEMENTS ###")
	end

	addPrint("")
	addPrint("### SKILLS ###")

	for i = 1, GetNumSkillLines() do
		skillName, header, _, skillRank, _, _, skillMaxRank = GetSkillLineInfo(i)
		if header == nil then
			addPrint(skillName .. ";" .. skillRank .. ";" .. skillMaxRank)
		end
	end
	
	addPrint("")
	addPrint("### EOF ###")
  
  local f = GetMainFrame(QEProfile)
  f:Show()

end


function GetMainFrame(text)
  -- Frame code largely adapted from https://www.wowinterface.com/forums/showpost.php?p=323901&postcount=2
  if not SimcFrame then
    -- Main Frame
    frameConfig = {
        point = "CENTER",
        relativeFrame = nil,
        relativePoint = "CENTER",
        ofsx = 0,
        ofsy = 0,
        width = 750,
        height = 400,
     }
    local f = CreateFrame("Frame", "SimcFrame", UIParent, "DialogBoxFrame")
    f:ClearAllPoints()
    -- load position from local DB
    f:SetPoint(
      frameConfig.point,
      frameConfig.relativeFrame,
      frameConfig.relativePoint,
      frameConfig.ofsx,
      frameConfig.ofsy
    )
    f:SetSize(frameConfig.width, frameConfig.height)
    f:SetBackdrop({
      bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
      edgeFile = "Interface\\PVPFrame\\UI-Character-PVP-Highlight",
      edgeSize = 16,
      insets = { left = 8, right = 8, top = 8, bottom = 8 },
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
      -- save position between sessions
      point, relativeFrame, relativeTo, ofsx, ofsy = self:GetPoint()
      frameConfig.point = point
      frameConfig.relativeFrame = relativeFrame
      frameConfig.relativePoint = relativeTo
      frameConfig.ofsx = ofsx
      frameConfig.ofsy = ofsy
    end)

    -- scroll frame
    local sf = CreateFrame("ScrollFrame", "SimcScrollFrame", f, "UIPanelScrollFrameTemplate")
    sf:SetPoint("LEFT", 16, 0)
    sf:SetPoint("RIGHT", -32, 0)
    sf:SetPoint("TOP", 0, -32)
    sf:SetPoint("BOTTOM", SimcFrameButton, "TOP", 0, 0)

    -- edit box
    local eb = CreateFrame("EditBox", "SimcEditBox", SimcScrollFrame)
    eb:SetSize(sf:GetSize())
    eb:SetMultiLine(true)
    eb:SetAutoFocus(true)
    eb:SetFontObject("ChatFontNormal")
    eb:SetScript("OnEscapePressed", function() f:Hide() end)
    sf:SetScrollChild(eb)

    -- resizing
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
            self:GetHighlightTexture():Hide() -- more noticeable
        end
    end)
    rb:SetScript("OnMouseUp", function(self, button)
        f:StopMovingOrSizing()
        self:GetHighlightTexture():Show()
        eb:SetWidth(sf:GetWidth())

        -- save size between sessions
        frameConfig.width = f:GetWidth()
        frameConfig.height = f:GetHeight()
    end)

    SimcFrame = f
  end
  SimcEditBox:SetText(text)
  SimcEditBox:HighlightText()
  return SimcFrame
end

function addPrint(line)
	--print(line)
	if line ~= nil then
		QEProfile = QEProfile .. line .. "\n";
	end
end

function convertSlot(raw)
	if (raw == "INVTYPE_HEAD") then return "head"
	elseif (raw == "INVTYPE_NECK") then return "neck" 
	elseif (raw == "INVTYPE_SHOULDER") then return "shoulder" 
	elseif (raw == "INVTYPE_CHEST") then return "chest" 
	elseif (raw == "INVTYPE_WAIST") then return "waist" 
	elseif (raw == "INVTYPE_LEGS") then return "legs" 
	elseif (raw == "INVTYPE_FEET") then return "feet" 
	elseif (raw == "INVTYPE_WRIST") then return "wrist" 
	elseif (raw == "INVTYPE_HAND") then return "hand" 
	elseif (raw == "INVTYPE_FINGER") then return "finger1" 
	elseif (raw == "INVTYPE_CLOAK") then return "back"
	elseif (raw == "INVTYPE_WEAPON") then return "one_hand"
	elseif (raw == "INVTYPE_SHIELD") then return "shield" 
	elseif (raw == "INVTYPE_2HWEAPON") then return "main_hand" 
	elseif (raw == "INVTYPE_WEAPONMAINHAND") then return "main_hand" 
	elseif (raw == "INVTYPE_WEAPONOFFHAND") then return "off_hand"
	elseif (raw == "INVTYPE_TRINKET") then return "trinket1" 
	elseif (raw == "INVTYPE_RELIC") then return "relic" 
	else return "unknown" end
end

SLASH_QE1 = "/qe";
SlashCmdList["QE"] = scanGear;




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

			--local _, enchantId, gem1, gem2, gem3, gem4 = string.match(itemLink, "item:(%d+):(%d+):(%d+):(%d+):(%d+):(%d+)")
			local enchantId = itemSplit[2]
			local gem1 = itemSplit[3]
			local gem2 = itemSplit[4]
			local gem3 = itemSplit[5]
			SocketInventoryItem(i)
			gemColors = {nil, nil, nil}
			for j=1, GetNumSockets() do
				_, _, gemColors[j] = GetExistingSocketInfo(j)
			end
			CloseSocketInfo()
			local itemName, _, _, _, _, _, _, _, _, _, _, classID, subclassID = GetItemInfo(equipID);
			--print(classID)
			if (classID == 2 or classID == 4) then
				addPrint(slotNames[i] .. "=,id=" .. equipID .. suffix .. ",enchantId=" .. enchantId .. ",gem1=" .. gem1 ..":" .. tostring(gemColors[1]) .. ",gem2=" .. gem2 ..":" .. tostring(gemColors[2]) .. ",gem3=" .. gem3 ..":" .. tostring(gemColors[3]))
				--print(itemName .. "(" .. itemType .. ")");
					
			end
		end
		
	end
	

	local ammoID = GetInventoryItemID("player", 0);
	if (ammoID ~= nil) then
		addPrint("ammo=,id=" .. ammoID)
	end
	if (pclass == "hunter") then
		local invID = ContainerIDToInventoryID(4)
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

	for bag=0, NUM_BAG_SLOTS do	
		
		for bagSlots=1, GetContainerNumSlots(bag) do
			--print("Inside the bag this time");
			local itemID = GetContainerItemID(bag, bagSlots);
			
			if (itemID) then 
				local itemName, _, itemRarity, itemLevel, itemMinLevel, itemType, itemSubType, itemStackCount, itemEquipLoc, itemTexture, vendorPrice, classID, subclassID = GetItemInfo(itemID);
				
				local itemLink = GetContainerItemLink(bag, bagSlots)
				local itemSplit = GetItemSplit(itemLink)
				local suffix = itemSplit[7] * -1
				local enchantId = itemSplit[2]
				local gem1 = itemSplit[3]
				local gem2 = itemSplit[4]
				local gem3 = itemSplit[5]
				
				if (suffix ~= -0) then
					local unique = bit.band(itemSplit[8], 65535)
					suffix = ",suffix=" .. suffix .. ",unique=" .. unique
				else suffix = "" end
				
				SocketContainerItem(bag, bagSlots)
				gemColors = {nil, nil, nil}
				for j=1, GetNumSockets() do
					_, _, gemColors[j] = GetExistingSocketInfo(j)
				end
				CloseSocketInfo()
				
				--if ((classID == 2 or classID == 4) and checkIfUsable(classID, subclassID)) then
				if (true or classID == 2 or classID == 4) then
					--addPrint("#")
					--addPrint("# " .. itemName)
					--addPrint("# " .. convertSlot(itemEquipLoc) .. "=,id=" .. itemID .. suffix)
					local _, itemCount = GetContainerItemInfo(bag, bagSlots)
					--addPrint(itemName)
					addPrint("id=" .. itemID .. suffix .. ",count=" .. itemCount .. ",enchantId=" .. enchantId .. ",gem1=" .. gem1 ..":" .. tostring(gemColors[1]) .. ",gem2=" .. gem2 ..":" .. tostring(gemColors[2]) .. ",gem3=" .. gem3 ..":" .. tostring(gemColors[3]))
					--print(itemName .. "(" .. itemType .. ")");
					
				end
			end
						
			--local _, _, itemRarity, _, _, itemType, itemSubType, _, _, _, _ = GetItemInfo()
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

	local Druid = {[33602] = true, [33891] = true, [33917] = true, [27013] = true, [24858] = true, [16864] = true, [33956] = true, [33831] = true, [17007] = true, [18562] = true, [27011] = true, [17055] = true, [17116] = true, [16979] = true, [17061] = true, [16880] = true, [17108] = true, [33600] = true, [33856] = true, [24894] = true, [33957] = true, [16857] = true, [16862] = true, [33873] = true, [33883] = true, [16689] = true, [16929] = true, [16949] = true, [33890] = true, [5570] = true, [17122] = true, [34300] = true, [17050] = true, [16847] = true, [16923] = true, [33869] = true, [17068] = true, [16812] = true, [16924] = true, [17078] = true, [17113] = true, [33591] = true, [17073] = true, [16931] = true, [17329] = true, [24977] = true, [33607] = true, [17118] = true, [17124] = true, [33597] = true, [37116] = true, [17063] = true, [17392] = true, [34153] = true, [34297] = true, [16835] = true, [16911] = true, [16930] = true, [16943] = true, [17065] = true, [37117] = true, [16814] = true, [16834] = true, [16840] = true, [16913] = true, [16942] = true, [17072] = true, [17119] = true, [27009] = true, [34151] = true, [16810] = true, [16813] = true, [16815] = true, [16816] = true, [16817] = true, [16910] = true, [16912] = true, [17002] = true, [17066] = true, [17067] = true, [17111] = true, [17390] = true, [17391] = true, [24866] = true, [24946] = true, [24974] = true, [33589] = true, [16858] = true, [17051] = true, [17074] = true, [17106] = true, [17120] = true, [17123] = true, [33590] = true, [16811] = true, [16819] = true, [16900] = true, [16934] = true, [17107] = true, [33872] = true, [33879] = true, [33880] = true, [34152] = true, [35364] = true, [16833] = true, [16947] = true, [16968] = true, [16972] = true, [17006] = true, [17058] = true, [17247] = true, [24969] = true, [24970] = true, [33601] = true, [33606] = true, [33889] = true, [16820] = true, [16822] = true, [16839] = true, [16845] = true, [16920] = true, [16935] = true, [16975] = true, [16998] = true, [17112] = true, [17121] = true, [24972] = true, [33604] = true, [33605] = true, [16846] = true, [16850] = true, [16859] = true, [16860] = true, [16861] = true, [16918] = true, [16919] = true, [16936] = true, [16937] = true, [16938] = true, [16940] = true, [16948] = true, [16999] = true, [17053] = true, [17054] = true, [17059] = true, [17060] = true, [17070] = true, [17075] = true, [17076] = true, [17077] = true, [17245] = true, [17248] = true, [24944] = true, [33592] = true, [33596] = true, [33851] = true, [33859] = true, [16836] = true, [16899] = true, [16901] = true, [16941] = true, [16974] = true, [17056] = true, [17071] = true, [24943] = true, [24968] = true, [33853] = true, [33866] = true, [33882] = true, [16818] = true, [16944] = true, [17003] = true, [17005] = true, [17104] = true, [33852] = true, [33855] = true, [33867] = true, [35363] = true, [16821] = true, [16896] = true, [16897] = true, [16909] = true, [16966] = true, [17004] = true, [17069] = true, [17249] = true, [24945] = true, [24971] = true, [24975] = true, [24976] = true, [33603] = true, [33886] = true, [33887] = true, [33599] = true, [33868] = true, [33881] = true, [33888] = true}
	local DruidVan = {[24977] = true, [17329] = true, [17392] = true, [24976] = true, [16813] = true, [17391] = true, [24975] = true, [16812] = true, [17390] = true, [24974] = true, [16811] = true, [16810] = true, [16940] = true, [16941] = true, [16857] = true, [17002] = true, [24866] = true, [16858] = true, [16859] = true, [16860] = true, [16861] = true, [16862] = true, [16979] = true, [16947] = true, [16948] = true, [16949] = true, [16950] = true, [16951] = true, [16934] = true, [16935] = true, [16936] = true, [16937] = true, [16938] = true, [17056] = true, [17058] = true, [17059] = true, [17060] = true, [17061] = true, [17104] = true, [24943] = true, [24944] = true, [24945] = true, [24946] = true, [17003] = true, [17004] = true, [17005] = true, [17006] = true, [24894] = true, [17079] = true, [17082] = true, [16918] = true, [16919] = true, [16920] = true, [17069] = true, [17070] = true, [17071] = true, [17072] = true, [17073] = true, [17050] = true, [17051] = true, [17053] = true, [17054] = true, [17055] = true, [16821] = true, [16822] = true, [16823] = true, [16824] = true, [16825] = true, [17245] = true, [17247] = true, [17248] = true, [17249] = true, [17074] = true, [17075] = true, [17076] = true, [17077] = true, [17078] = true, [17111] = true, [17112] = true, [17113] = true, [16966] = true, [16968] = true, [16850] = true, [16923] = true, [16924] = true, [16925] = true, [16926] = true, [16836] = true, [16839] = true, [16840] = true, [17123] = true, [17124] = true, [16814] = true, [16815] = true, [16816] = true, [16817] = true, [16818] = true, [5570] = true, [17007] = true, [16896] = true, [16897] = true, [16899] = true, [16900] = true, [16901] = true, [16845] = true, [16846] = true, [16847] = true, [24858] = true, [16833] = true, [16834] = true, [16835] = true, [16902] = true, [16903] = true, [16904] = true, [16905] = true, [16906] = true, [17063] = true, [17065] = true, [17066] = true, [17067] = true, [17068] = true, [16880] = true, [16689] = true, [16819] = true, [16820] = true, [17116] = true, [16864] = true, [16972] = true, [16974] = true, [16975] = true, [16961] = true, [17106] = true, [17107] = true, [17108] = true, [16998] = true, [16999] = true, [16942] = true, [16943] = true, [16944] = true, [17118] = true, [17119] = true, [17120] = true, [17121] = true, [17122] = true, [18562] = true, [16929] = true, [16930] = true, [16931] = true, [16932] = true, [16933] = true, [24968] = true, [24969] = true, [24970] = true, [24971] = true, [24972] = true, [16909] = true, [16910] = true, [16911] = true, [16912] = true, [16913] = true}
	local Hunter = {[34503] = true, [34460] = true, [19425] = true, [27065] = true, [19574] = true, [27066] = true, [34954] = true, [19263] = true, [19294] = true, [23989] = true, [34692] = true, [19577] = true, [19434] = true, [19490] = true, [34839] = true, [19503] = true, [19420] = true, [20904] = true, [34490] = true, [34948] = true, [19623] = true, [27068] = true, [19596] = true, [19386] = true, [19388] = true, [19573] = true, [19290] = true, [19306] = true, [19556] = true, [19620] = true, [19625] = true, [34470] = true, [35030] = true, [19245] = true, [19592] = true, [20906] = true, [19454] = true, [19467] = true, [19500] = true, [19612] = true, [34459] = true, [24283] = true, [19376] = true, [19506] = true, [19511] = true, [19610] = true, [34500] = true, [19232] = true, [19233] = true, [19371] = true, [19424] = true, [19427] = true, [19458] = true, [19465] = true, [19466] = true, [19508] = true, [19509] = true, [19510] = true, [19552] = true, [19575] = true, [20895] = true, [27067] = true, [34454] = true, [19152] = true, [19160] = true, [19180] = true, [19181] = true, [19184] = true, [19257] = true, [19258] = true, [19297] = true, [19301] = true, [19412] = true, [19413] = true, [19414] = true, [19423] = true, [19429] = true, [19430] = true, [19583] = true, [19584] = true, [19587] = true, [19619] = true, [34455] = true, [34949] = true, [19416] = true, [19422] = true, [19461] = true, [19507] = true, [19609] = true, [34493] = true, [19159] = true, [19239] = true, [19421] = true, [19431] = true, [19457] = true, [19485] = true, [19549] = true, [19555] = true, [19560] = true, [19586] = true, [19617] = true, [19621] = true, [19624] = true, [34465] = true, [19151] = true, [19228] = true, [19286] = true, [19407] = true, [19418] = true, [19426] = true, [19488] = true, [19550] = true, [19551] = true, [19553] = true, [19554] = true, [19572] = true, [19585] = true, [19590] = true, [19599] = true, [19600] = true, [19601] = true, [19618] = true, [19622] = true, [20902] = true, [19153] = true, [19287] = true, [19298] = true, [19415] = true, [19417] = true, [19455] = true, [19456] = true, [19462] = true, [19487] = true, [19489] = true, [19498] = true, [19499] = true, [19559] = true, [19578] = true, [34464] = true, [34476] = true, [34484] = true, [35102] = true, [35103] = true, [19256] = true, [19295] = true, [19300] = true, [19370] = true, [19373] = true, [19387] = true, [19419] = true, [19598] = true, [19602] = true, [19616] = true, [24297] = true, [34482] = true, [34488] = true, [34494] = true, [19377] = true, [19468] = true, [20903] = true, [20909] = true, [24133] = true, [24691] = true, [34466] = true, [34469] = true, [34485] = true, [34486] = true, [34487] = true, [34496] = true, [34497] = true, [34508] = true, [35100] = true, [35104] = true, [19255] = true, [19259] = true, [19464] = true, [34467] = true, [34468] = true, [34492] = true, [34502] = true, [35029] = true, [35110] = true, [19168] = true, [20905] = true, [20910] = true, [24132] = true, [24293] = true, [24294] = true, [24296] = true, [34462] = true, [34475] = true, [34483] = true, [34489] = true, [34491] = true, [34498] = true, [34499] = true, [34506] = true, [34950] = true, [20900] = true, [20901] = true, [24295] = true, [24443] = true, [34453] = true, [34507] = true, [34838] = true, [35111] = true}
	local HunterVan = {[20904] = true, [24133] = true, [20910] = true, [20903] = true, [24132] = true, [20902] = true, [20909] = true, [20901] = true, [20900] = true, [19434] = true, [19461] = true, [19462] = true, [24691] = true, [19590] = true, [19592] = true, [19596] = true, [19574] = true, [19239] = true, [19245] = true, [19306] = true, [19295] = true, [19297] = true, [19298] = true, [19300] = true, [19301] = true, [19263] = true, [19416] = true, [19417] = true, [19418] = true, [19419] = true, [19420] = true, [19583] = true, [19584] = true, [19585] = true, [19586] = true, [19587] = true, [19184] = true, [19387] = true, [19388] = true, [19389] = true, [19390] = true, [19598] = true, [19599] = true, [19600] = true, [19601] = true, [19602] = true, [19621] = true, [19622] = true, [19623] = true, [19624] = true, [19625] = true, [19498] = true, [19499] = true, [19500] = true, [19151] = true, [19152] = true, [19153] = true, [19454] = true, [19455] = true, [19456] = true, [19457] = true, [19458] = true, [19552] = true, [19553] = true, [19554] = true, [19555] = true, [19556] = true, [19549] = true, [19550] = true, [19551] = true, [24386] = true, [24387] = true, [19407] = true, [19412] = true, [19413] = true, [19414] = true, [19415] = true, [19557] = true, [19558] = true, [19286] = true, [19287] = true, [19421] = true, [19422] = true, [19423] = true, [19424] = true, [19425] = true, [19572] = true, [19573] = true, [19575] = true, [24443] = true, [19491] = true, [19493] = true, [19494] = true, [19464] = true, [19465] = true, [19466] = true, [19467] = true, [19468] = true, [19228] = true, [19232] = true, [19233] = true, [19234] = true, [19235] = true, [19577] = true, [19370] = true, [19371] = true, [19373] = true, [19426] = true, [19427] = true, [19429] = true, [19430] = true, [19431] = true, [19168] = true, [19180] = true, [19181] = true, [24296] = true, [24297] = true, [24293] = true, [24294] = true, [24295] = true, [19485] = true, [19487] = true, [19488] = true, [19489] = true, [19490] = true, [19559] = true, [19560] = true, [19507] = true, [19508] = true, [19509] = true, [19510] = true, [19511] = true, [19159] = true, [19160] = true, [19503] = true, [19578] = true, [20895] = true, [19290] = true, [19294] = true, [24283] = true, [19255] = true, [19256] = true, [19257] = true, [19258] = true, [19259] = true, [19609] = true, [19610] = true, [19612] = true, [19376] = true, [19377] = true, [19506] = true, [19616] = true, [19617] = true, [19618] = true, [19619] = true, [19620] = true, [19386] = true}
	local Mage = {[12472] = true, [31687] = true, [12042] = true, [12873] = true, [31661] = true, [29440] = true, [12043] = true, [31589] = true, [11426] = true, [12985] = true, [11958] = true, [33938] = true, [12488] = true, [12592] = true, [11129] = true, [12497] = true, [33043] = true, [31680] = true, [12842] = true, [12571] = true, [12577] = true, [11366] = true, [31686] = true, [33933] = true, [12848] = true, [18464] = true, [33405] = true, [15053] = true, [31583] = true, [29447] = true, [12503] = true, [12846] = true, [12526] = true, [12872] = true, [28595] = true, [12982] = true, [11071] = true, [12606] = true, [13021] = true, [12505] = true, [12522] = true, [12524] = true, [12525] = true, [12598] = true, [35581] = true, [31640] = true, [11210] = true, [12523] = true, [12605] = true, [31588] = true, [13043] = true, [12360] = true, [18809] = true, [27132] = true, [11185] = true, [12469] = true, [13018] = true, [13019] = true, [13020] = true, [31660] = true, [11180] = true, [12341] = true, [12353] = true, [12840] = true, [12953] = true, [13033] = true, [18460] = true, [28592] = true, [31642] = true, [33042] = true, [11113] = true, [12350] = true, [12952] = true, [16766] = true, [16770] = true, [27133] = true, [11170] = true, [12338] = true, [12342] = true, [12359] = true, [12500] = true, [12519] = true, [12983] = true, [13031] = true, [29076] = true, [31674] = true, [31678] = true, [33041] = true, [6085] = true, [11094] = true, [11095] = true, [12378] = true, [12400] = true, [12490] = true, [12672] = true, [13032] = true, [15060] = true, [16757] = true, [27134] = true, [31575] = true, [12339] = true, [12340] = true, [12349] = true, [12351] = true, [12357] = true, [12358] = true, [12399] = true, [12463] = true, [12464] = true, [12467] = true, [12473] = true, [12487] = true, [12489] = true, [12496] = true, [12501] = true, [12502] = true, [12518] = true, [12569] = true, [12574] = true, [12575] = true, [12576] = true, [12839] = true, [12841] = true, [12847] = true, [16758] = true, [18459] = true, [31573] = true, [31579] = true, [31672] = true, [31676] = true, [11083] = true, [11252] = true, [12475] = true, [12984] = true, [15058] = true, [18463] = true, [28574] = true, [28593] = true, [29441] = true, [31572] = true, [34296] = true, [6057] = true, [11078] = true, [11115] = true, [11119] = true, [11165] = true, [11175] = true, [11213] = true, [15047] = true, [15052] = true, [15059] = true, [16763] = true, [16765] = true, [16769] = true, [31584] = true, [31587] = true, [31679] = true, [11108] = true, [11207] = true, [11237] = true, [11367] = true, [12398] = true, [18462] = true, [28332] = true, [29438] = true, [29444] = true, [31669] = true, [31677] = true, [31684] = true, [31685] = true, [11069] = true, [11070] = true, [11080] = true, [11100] = true, [11120] = true, [11124] = true, [11151] = true, [11160] = true, [11189] = true, [11222] = true, [11247] = true, [11368] = true, [31639] = true, [31659] = true, [31670] = true, [31675] = true, [31682] = true, [31683] = true, [34295] = true, [11103] = true, [11190] = true, [11242] = true, [31569] = true, [31570] = true, [31658] = true, [31667] = true, [35578] = true, [11232] = true, [11255] = true, [28594] = true, [29074] = true, [31571] = true, [31585] = true, [31641] = true, [31656] = true, [31668] = true, [34293] = true, [29075] = true, [29439] = true, [29445] = true, [29446] = true, [31574] = true, [31582] = true, [31586] = true, [31638] = true, [31657] = true}
	local MageVan = {[13021] = true, [18809] = true, [13033] = true, [12526] = true, [13020] = true, [13032] = true, [12525] = true, [13031] = true, [13019] = true, [12524] = true, [13018] = true, [12523] = true, [12522] = true, [12505] = true, [11213] = true, [12574] = true, [12575] = true, [12576] = true, [12577] = true, [11222] = true, [12839] = true, [12840] = true, [12841] = true, [12842] = true, [15058] = true, [15059] = true, [15060] = true, [18462] = true, [18463] = true, [18464] = true, [11232] = true, [12500] = true, [12501] = true, [12502] = true, [12503] = true, [12042] = true, [28574] = true, [11210] = true, [12592] = true, [16757] = true, [16758] = true, [11113] = true, [11083] = true, [12351] = true, [12472] = true, [11129] = true, [11115] = true, [11367] = true, [11368] = true, [29438] = true, [29439] = true, [29440] = true, [11124] = true, [12378] = true, [12398] = true, [12399] = true, [12400] = true, [11100] = true, [12353] = true, [11160] = true, [12518] = true, [12519] = true, [11189] = true, [28332] = true, [11071] = true, [12496] = true, [12497] = true, [11426] = true, [11958] = true, [11207] = true, [12672] = true, [15047] = true, [15052] = true, [15053] = true, [11119] = true, [11120] = true, [12846] = true, [12847] = true, [12848] = true, [11103] = true, [12357] = true, [12358] = true, [12359] = true, [12360] = true, [11242] = true, [12467] = true, [12469] = true, [11237] = true, [12463] = true, [12464] = true, [16769] = true, [16770] = true, [11185] = true, [12487] = true, [12488] = true, [11190] = true, [12489] = true, [12490] = true, [11255] = true, [12598] = true, [11078] = true, [11080] = true, [12342] = true, [11094] = true, [13043] = true, [11069] = true, [12338] = true, [12339] = true, [12340] = true, [12341] = true, [11108] = true, [12349] = true, [12350] = true, [11165] = true, [12475] = true, [11070] = true, [12473] = true, [16763] = true, [16765] = true, [16766] = true, [11252] = true, [12605] = true, [11095] = true, [12872] = true, [12873] = true, [18459] = true, [18460] = true, [29441] = true, [29444] = true, [29445] = true, [29446] = true, [29447] = true, [11247] = true, [12606] = true, [29074] = true, [29075] = true, [29076] = true, [11175] = true, [12569] = true, [12571] = true, [11151] = true, [12952] = true, [12953] = true, [12043] = true, [11366] = true, [11170] = true, [12982] = true, [12983] = true, [12984] = true, [12985] = true, [6057] = true, [6085] = true, [11180] = true, [28592] = true, [28593] = true, [28594] = true, [28595] = true}
	local Paladin = {[35395] = true, [20217] = true, [27179] = true, [20218] = true, [27168] = true, [27170] = true, [31821] = true, [20337] = true, [32700] = true, [31935] = true, [31850] = true, [31870] = true, [31842] = true, [44414] = true, [20182] = true, [20375] = true, [31849] = true, [31841] = true, [20473] = true, [33072] = true, [20216] = true, [20470] = true, [20914] = true, [20059] = true, [20066] = true, [26021] = true, [31854] = true, [20266] = true, [20137] = true, [20256] = true, [31836] = true, [31878] = true, [20175] = true, [20911] = true, [20215] = true, [31830] = true, [20200] = true, [20235] = true, [31862] = true, [20121] = true, [20925] = true, [20100] = true, [20105] = true, [20150] = true, [20048] = true, [31826] = true, [31845] = true, [31868] = true, [31883] = true, [25988] = true, [31847] = true, [20127] = true, [9452] = true, [20142] = true, [25957] = true, [26022] = true, [32699] = true, [20254] = true, [20920] = true, [31828] = true, [20468] = true, [20928] = true, [26023] = true, [27174] = true, [20205] = true, [20206] = true, [20332] = true, [20912] = true, [20919] = true, [31873] = true, [31848] = true, [35397] = true, [20064] = true, [20092] = true, [20138] = true, [35396] = true, [20091] = true, [20147] = true, [20335] = true, [20918] = true, [31833] = true, [31837] = true, [20042] = true, [20045] = true, [20049] = true, [20099] = true, [20113] = true, [20174] = true, [20179] = true, [20239] = true, [20261] = true, [20262] = true, [20489] = true, [20927] = true, [31822] = true, [31882] = true, [9799] = true, [20096] = true, [20101] = true, [20207] = true, [20209] = true, [20214] = true, [20487] = true, [20915] = true, [25956] = true, [31844] = true, [31852] = true, [31871] = true, [31881] = true, [5923] = true, [5924] = true, [5925] = true, [5926] = true, [20058] = true, [20120] = true, [20139] = true, [20177] = true, [20208] = true, [20469] = true, [20913] = true, [25836] = true, [31858] = true, [31872] = true, [20148] = true, [20245] = true, [20257] = true, [20929] = true, [25829] = true, [26016] = true, [31835] = true, [31869] = true, [41026] = true, [9453] = true, [20046] = true, [20060] = true, [20062] = true, [20136] = true, [20143] = true, [20144] = true, [20149] = true, [20180] = true, [20213] = true, [20237] = true, [20244] = true, [20258] = true, [20336] = true, [20360] = true, [20361] = true, [31823] = true, [31824] = true, [31853] = true, [31859] = true, [31860] = true, [31879] = true, [20056] = true, [20057] = true, [20097] = true, [20098] = true, [20117] = true, [20140] = true, [20181] = true, [20198] = true, [20210] = true, [20224] = true, [20234] = true, [20238] = true, [20255] = true, [20264] = true, [20265] = true, [20331] = true, [31825] = true, [31829] = true, [31846] = true, [31866] = true, [31867] = true, [31876] = true, [32043] = true, [41021] = true, [20047] = true, [20061] = true, [20063] = true, [20102] = true, [20103] = true, [20104] = true, [20111] = true, [20112] = true, [20118] = true, [20119] = true, [20130] = true, [20135] = true, [20141] = true, [20145] = true, [20146] = true, [20196] = true, [20197] = true, [20199] = true, [20212] = true, [20225] = true, [20259] = true, [20260] = true, [20263] = true, [20330] = true, [20359] = true, [20488] = true, [20930] = true, [31838] = true, [31839] = true, [31840] = true, [31851] = true, [31861] = true, [31877] = true, [31880] = true}
	local PaladinVan = {[20914] = true, [20924] = true, [20928] = true, [20920] = true, [20930] = true, [20913] = true, [20923] = true, [20927] = true, [20919] = true, [20929] = true, [20912] = true, [20922] = true, [20918] = true, [20116] = true, [20915] = true, [20096] = true, [20097] = true, [20098] = true, [20099] = true, [20100] = true, [20101] = true, [20102] = true, [20103] = true, [20104] = true, [20105] = true, [20217] = true, [20911] = true, [26573] = true, [20117] = true, [20118] = true, [20119] = true, [20120] = true, [20121] = true, [20060] = true, [20061] = true, [20062] = true, [20063] = true, [20064] = true, [20216] = true, [20257] = true, [20258] = true, [20259] = true, [20260] = true, [20261] = true, [20262] = true, [20263] = true, [20264] = true, [20265] = true, [20266] = true, [9799] = true, [25988] = true, [20174] = true, [20175] = true, [20237] = true, [20238] = true, [20239] = true, [5923] = true, [5924] = true, [5925] = true, [5926] = true, [25829] = true, [20925] = true, [20473] = true, [20210] = true, [20212] = true, [20213] = true, [20214] = true, [20215] = true, [20042] = true, [20045] = true, [20046] = true, [20047] = true, [20048] = true, [20244] = true, [20245] = true, [20254] = true, [20255] = true, [20256] = true, [20138] = true, [20139] = true, [20140] = true, [20141] = true, [20142] = true, [20487] = true, [20488] = true, [20489] = true, [25956] = true, [25957] = true, [20234] = true, [20235] = true, [20091] = true, [20092] = true, [20468] = true, [20469] = true, [20470] = true, [20224] = true, [20225] = true, [20330] = true, [20331] = true, [20332] = true, [20335] = true, [20336] = true, [20337] = true, [20359] = true, [20360] = true, [20361] = true, [20196] = true, [20197] = true, [20198] = true, [20199] = true, [20200] = true, [26022] = true, [26023] = true, [20177] = true, [20179] = true, [20180] = true, [20181] = true, [20182] = true, [20127] = true, [20130] = true, [20135] = true, [20136] = true, [20137] = true, [20066] = true, [20218] = true, [20375] = true, [20148] = true, [20149] = true, [20150] = true, [20205] = true, [20206] = true, [20207] = true, [20208] = true, [20209] = true, [20143] = true, [20144] = true, [20145] = true, [20146] = true, [20147] = true, [20111] = true, [20112] = true, [20113] = true, [9453] = true, [25836] = true, [20049] = true, [20056] = true, [20057] = true, [20058] = true, [20059] = true, [9452] = true, [26016] = true, [26021] = true}
	local Priest = {[35395] = true, [20217] = true, [27179] = true, [20218] = true, [27168] = true, [27170] = true, [31821] = true, [20337] = true, [32700] = true, [31935] = true, [31850] = true, [31870] = true, [31842] = true, [44414] = true, [20182] = true, [20375] = true, [31849] = true, [31841] = true, [20473] = true, [33072] = true, [20216] = true, [20470] = true, [20914] = true, [20059] = true, [20066] = true, [26021] = true, [31854] = true, [20266] = true, [20137] = true, [20256] = true, [31836] = true, [31878] = true, [20175] = true, [20911] = true, [20215] = true, [31830] = true, [20200] = true, [20235] = true, [31862] = true, [20121] = true, [20925] = true, [20100] = true, [20105] = true, [20150] = true, [20048] = true, [31826] = true, [31845] = true, [31868] = true, [31883] = true, [25988] = true, [31847] = true, [20127] = true, [9452] = true, [20142] = true, [25957] = true, [26022] = true, [32699] = true, [20254] = true, [20920] = true, [31828] = true, [20468] = true, [20928] = true, [26023] = true, [27174] = true, [20205] = true, [20206] = true, [20332] = true, [20912] = true, [20919] = true, [31873] = true, [31848] = true, [35397] = true, [20064] = true, [20092] = true, [20138] = true, [35396] = true, [20091] = true, [20147] = true, [20335] = true, [20918] = true, [31833] = true, [31837] = true, [20042] = true, [20045] = true, [20049] = true, [20099] = true, [20113] = true, [20174] = true, [20179] = true, [20239] = true, [20261] = true, [20262] = true, [20489] = true, [20927] = true, [31822] = true, [31882] = true, [9799] = true, [20096] = true, [20101] = true, [20207] = true, [20209] = true, [20214] = true, [20487] = true, [20915] = true, [25956] = true, [31844] = true, [31852] = true, [31871] = true, [31881] = true, [5923] = true, [5924] = true, [5925] = true, [5926] = true, [20058] = true, [20120] = true, [20139] = true, [20177] = true, [20208] = true, [20469] = true, [20913] = true, [25836] = true, [31858] = true, [31872] = true, [20148] = true, [20245] = true, [20257] = true, [20929] = true, [25829] = true, [26016] = true, [31835] = true, [31869] = true, [41026] = true, [9453] = true, [20046] = true, [20060] = true, [20062] = true, [20136] = true, [20143] = true, [20144] = true, [20149] = true, [20180] = true, [20213] = true, [20237] = true, [20244] = true, [20258] = true, [20336] = true, [20360] = true, [20361] = true, [31823] = true, [31824] = true, [31853] = true, [31859] = true, [31860] = true, [31879] = true, [20056] = true, [20057] = true, [20097] = true, [20098] = true, [20117] = true, [20140] = true, [20181] = true, [20198] = true, [20210] = true, [20224] = true, [20234] = true, [20238] = true, [20255] = true, [20264] = true, [20265] = true, [20331] = true, [31825] = true, [31829] = true, [31846] = true, [31866] = true, [31867] = true, [31876] = true, [32043] = true, [41021] = true, [20047] = true, [20061] = true, [20063] = true, [20102] = true, [20103] = true, [20104] = true, [20111] = true, [20112] = true, [20118] = true, [20119] = true, [20130] = true, [20135] = true, [20141] = true, [20145] = true, [20146] = true, [20196] = true, [20197] = true, [20199] = true, [20212] = true, [20225] = true, [20259] = true, [20260] = true, [20263] = true, [20330] = true, [20359] = true, [20488] = true, [20930] = true, [31838] = true, [31839] = true, [31840] = true, [31851] = true, [31861] = true, [31877] = true, [31880] = true}
	local PriestVan = {[27841] = true, [27801] = true, [27871] = true, [18807] = true, [27800] = true, [17314] = true, [14819] = true, [27870] = true, [27799] = true, [17313] = true, [14818] = true, [15431] = true, [17312] = true, [15430] = true, [17311] = true, [15268] = true, [15323] = true, [15324] = true, [15325] = true, [15326] = true, [27811] = true, [27815] = true, [27816] = true, [15259] = true, [15307] = true, [15308] = true, [15309] = true, [15310] = true, [18530] = true, [18531] = true, [18533] = true, [18534] = true, [18535] = true, [14752] = true, [18544] = true, [18547] = true, [18548] = true, [18549] = true, [18550] = true, [14913] = true, [15012] = true, [15237] = true, [27789] = true, [27790] = true, [14889] = true, [15008] = true, [15009] = true, [15010] = true, [15011] = true, [15274] = true, [15311] = true, [14912] = true, [15013] = true, [15014] = true, [14747] = true, [14770] = true, [14771] = true, [14750] = true, [14772] = true, [15273] = true, [15312] = true, [15313] = true, [15314] = true, [15316] = true, [14749] = true, [14767] = true, [14748] = true, [14768] = true, [14769] = true, [14911] = true, [15018] = true, [15392] = true, [15448] = true, [14908] = true, [15020] = true, [17191] = true, [15275] = true, [15317] = true, [27839] = true, [27840] = true, [14751] = true, [14892] = true, [15362] = true, [15363] = true, [724] = true, [14531] = true, [14774] = true, [14521] = true, [14776] = true, [14777] = true, [14520] = true, [14780] = true, [14781] = true, [14782] = true, [14783] = true, [18551] = true, [18552] = true, [18553] = true, [18554] = true, [18555] = true, [15407] = true, [10060] = true, [14909] = true, [15017] = true, [15272] = true, [15318] = true, [15320] = true, [15260] = true, [15327] = true, [15328] = true, [17322] = true, [17323] = true, [17325] = true, [15257] = true, [15331] = true, [15332] = true, [15333] = true, [15334] = true, [15473] = true, [15487] = true, [14523] = true, [14784] = true, [14785] = true, [14786] = true, [14787] = true, [27900] = true, [27901] = true, [27902] = true, [27903] = true, [27904] = true, [20711] = true, [15270] = true, [15335] = true, [15336] = true, [15337] = true, [15338] = true, [14901] = true, [15028] = true, [15029] = true, [15030] = true, [15031] = true, [14898] = true, [15349] = true, [15354] = true, [15355] = true, [15356] = true, [14522] = true, [14788] = true, [14789] = true, [14790] = true, [14791] = true, [15286] = true, [14524] = true, [14525] = true, [14526] = true, [14527] = true, [14528] = true}
	local Rogue = {[36554] = true, [14169] = true, [31230] = true, [1329] = true, [35553] = true, [16511] = true, [13877] = true, [13964] = true, [26864] = true, [30920] = true, [13750] = true, [14179] = true, [13845] = true, [14251] = true, [14278] = true, [14173] = true, [13852] = true, [13973] = true, [31209] = true, [13803] = true, [31223] = true, [14094] = true, [14185] = true, [31213] = true, [32601] = true, [35551] = true, [14183] = true, [14177] = true, [14065] = true, [16720] = true, [14062] = true, [14137] = true, [14148] = true, [30906] = true, [31220] = true, [14138] = true, [14161] = true, [13875] = true, [14070] = true, [14160] = true, [31245] = true, [13853] = true, [13855] = true, [13867] = true, [13872] = true, [13958] = true, [13970] = true, [14064] = true, [14167] = true, [14195] = true, [17348] = true, [31124] = true, [13706] = true, [13832] = true, [13844] = true, [13972] = true, [14071] = true, [14159] = true, [14171] = true, [30895] = true, [13733] = true, [13792] = true, [13801] = true, [13802] = true, [13866] = true, [13976] = true, [14066] = true, [14142] = true, [14166] = true, [13705] = true, [13715] = true, [13788] = true, [13789] = true, [13790] = true, [13800] = true, [13865] = true, [13971] = true, [13979] = true, [13983] = true, [14072] = true, [14073] = true, [14074] = true, [14132] = true, [14136] = true, [14140] = true, [14141] = true, [14144] = true, [14156] = true, [14158] = true, [14165] = true, [14193] = true, [14194] = true, [16719] = true, [13804] = true, [13849] = true, [13856] = true, [13863] = true, [13975] = true, [14063] = true, [14076] = true, [14081] = true, [14082] = true, [14113] = true, [14128] = true, [14135] = true, [14162] = true, [14172] = true, [31212] = true, [31228] = true, [13712] = true, [13843] = true, [13851] = true, [13960] = true, [13962] = true, [13980] = true, [14079] = true, [14080] = true, [14083] = true, [14168] = true, [14175] = true, [14186] = true, [14983] = true, [16514] = true, [16515] = true, [30919] = true, [31126] = true, [31130] = true, [35550] = true, [13713] = true, [13741] = true, [13743] = true, [13754] = true, [13793] = true, [13805] = true, [13806] = true, [13848] = true, [13854] = true, [13961] = true, [13963] = true, [13981] = true, [14114] = true, [14116] = true, [14164] = true, [14174] = true, [16513] = true, [18429] = true, [31131] = true, [31227] = true, [13709] = true, [13742] = true, [13791] = true, [13807] = true, [14075] = true, [14176] = true, [17347] = true, [18428] = true, [31211] = true, [14057] = true, [14117] = true, [14163] = true, [18427] = true, [31226] = true, [31233] = true, [31384] = true, [13732] = true, [14115] = true, [14139] = true, [14190] = true, [30894] = true, [31242] = true, [30892] = true, [30904] = true, [31123] = true, [31222] = true, [31244] = true, [31385] = true, [35552] = true, [30893] = true, [30902] = true, [31216] = true, [31219] = true, [31382] = true, [35541] = true, [31122] = true, [31208] = true, [31218] = true, [31239] = true, [31241] = true, [30903] = true, [30905] = true, [31217] = true, [31221] = true, [31229] = true, [31240] = true, [31380] = true, [31383] = true}
	local RogueVan = {[17348] = true, [17347] = true, [13750] = true, [18427] = true, [18428] = true, [18429] = true, [13877] = true, [13975] = true, [14062] = true, [14063] = true, [14064] = true, [14065] = true, [14177] = true, [13706] = true, [13804] = true, [13805] = true, [13806] = true, [13807] = true, [30902] = true, [30903] = true, [30904] = true, [30905] = true, [30906] = true, [13713] = true, [13853] = true, [13854] = true, [13855] = true, [13856] = true, [14082] = true, [14083] = true, [13715] = true, [13848] = true, [13849] = true, [13851] = true, [13852] = true, [13981] = true, [14066] = true, [13742] = true, [13872] = true, [14278] = true, [30894] = true, [30895] = true, [16511] = true, [14079] = true, [14080] = true, [14081] = true, [13733] = true, [13865] = true, [13866] = true, [14162] = true, [14163] = true, [14164] = true, [14168] = true, [14169] = true, [13741] = true, [13792] = true, [13793] = true, [13754] = true, [13867] = true, [14174] = true, [14175] = true, [14176] = true, [14113] = true, [14114] = true, [14115] = true, [14116] = true, [14117] = true, [14076] = true, [14094] = true, [13732] = true, [13863] = true, [14165] = true, [14166] = true, [14167] = true, [13743] = true, [13875] = true, [13976] = true, [13979] = true, [13980] = true, [14128] = true, [14132] = true, [14135] = true, [14136] = true, [14137] = true, [13712] = true, [13788] = true, [13789] = true, [13790] = true, [13791] = true, [13709] = true, [13800] = true, [13801] = true, [13802] = true, [13803] = true, [14138] = true, [14139] = true, [14140] = true, [14141] = true, [14142] = true, [13958] = true, [13970] = true, [13971] = true, [13972] = true, [13973] = true, [14158] = true, [14159] = true, [14057] = true, [14072] = true, [14073] = true, [14074] = true, [14075] = true, [13705] = true, [13832] = true, [13843] = true, [13844] = true, [13845] = true, [14183] = true, [14185] = true, [14179] = true, [14144] = true, [14148] = true, [14251] = true, [14156] = true, [14160] = true, [14161] = true, [14186] = true, [14190] = true, [14193] = true, [14194] = true, [14195] = true, [14171] = true, [14172] = true, [14173] = true, [13983] = true, [14070] = true, [14071] = true, [30892] = true, [30893] = true, [13960] = true, [13961] = true, [13962] = true, [13963] = true, [13964] = true, [14983] = true, [16513] = true, [16514] = true, [16515] = true, [16719] = true, [16720] = true, [30919] = true, [30920] = true}
	local Shaman = {[30706] = true, [17364] = true, [30798] = true, [30811] = true, [974] = true, [16190] = true, [30823] = true, [16166] = true, [16240] = true, [30884] = true, [16164] = true, [32594] = true, [30802] = true, [16188] = true, [29202] = true, [29193] = true, [16221] = true, [16198] = true, [29080] = true, [29065] = true, [16089] = true, [16268] = true, [43338] = true, [30814] = true, [16309] = true, [28998] = true, [16213] = true, [29180] = true, [16209] = true, [16284] = true, [32593] = true, [29206] = true, [16116] = true, [29191] = true, [30681] = true, [16038] = true, [16161] = true, [16187] = true, [16256] = true, [16258] = true, [30886] = true, [16259] = true, [16287] = true, [16295] = true, [16108] = true, [16112] = true, [16301] = true, [16305] = true, [17489] = true, [30881] = true, [16130] = true, [16173] = true, [16225] = true, [16180] = true, [16255] = true, [16266] = true, [16582] = true, [29192] = true, [30816] = true, [16176] = true, [16303] = true, [17485] = true, [30679] = true, [30867] = true, [16120] = true, [16302] = true, [16544] = true, [28996] = true, [30864] = true, [16039] = true, [16086] = true, [16181] = true, [16196] = true, [30666] = true, [16035] = true, [16041] = true, [16210] = true, [16217] = true, [16106] = true, [16109] = true, [16224] = true, [16262] = true, [16304] = true, [16578] = true, [30869] = true, [16113] = true, [16114] = true, [16194] = true, [16205] = true, [16206] = true, [16212] = true, [16214] = true, [16215] = true, [16216] = true, [16219] = true, [16220] = true, [16223] = true, [16229] = true, [16252] = true, [16254] = true, [16274] = true, [16290] = true, [16299] = true, [16306] = true, [16307] = true, [16308] = true, [16580] = true, [16581] = true, [30160] = true, [30674] = true, [16208] = true, [16218] = true, [16222] = true, [16228] = true, [16230] = true, [16232] = true, [16261] = true, [29187] = true, [30668] = true, [30673] = true, [30813] = true, [16107] = true, [16110] = true, [16111] = true, [16117] = true, [16179] = true, [16207] = true, [16233] = true, [16234] = true, [16272] = true, [29179] = true, [30819] = true, [16040] = true, [16043] = true, [16105] = true, [16115] = true, [16118] = true, [16119] = true, [16160] = true, [16178] = true, [16211] = true, [16226] = true, [16227] = true, [16235] = true, [16271] = true, [16273] = true, [16282] = true, [16283] = true, [16293] = true, [16300] = true, [16579] = true, [17486] = true, [17487] = true, [17488] = true, [30678] = true, [30812] = true, [16182] = true, [16184] = true, [16281] = true, [29000] = true, [29087] = true, [30665] = true, [30675] = true, [29088] = true, [30809] = true, [30868] = true, [30885] = true, [28997] = true, [29062] = true, [29082] = true, [29086] = true, [30664] = true, [30667] = true, [30672] = true, [30818] = true, [29064] = true, [29189] = true, [30810] = true, [30865] = true, [30866] = true, [28999] = true, [29079] = true, [29084] = true, [29205] = true, [30680] = true, [30808] = true, [30872] = true, [30873] = true, [30883] = true}
	local ShamanVan = {[17359] = true, [17354] = true, [16176] = true, [16235] = true, [16240] = true, [17485] = true, [17486] = true, [17487] = true, [17488] = true, [17489] = true, [16254] = true, [16271] = true, [16272] = true, [16273] = true, [16274] = true, [16038] = true, [16160] = true, [16161] = true, [16041] = true, [16117] = true, [16118] = true, [16119] = true, [16120] = true, [16035] = true, [16105] = true, [16106] = true, [16107] = true, [16108] = true, [16039] = true, [16109] = true, [16110] = true, [16111] = true, [16112] = true, [16043] = true, [16130] = true, [29179] = true, [29180] = true, [30160] = true, [16164] = true, [16089] = true, [16166] = true, [28996] = true, [28997] = true, [28998] = true, [16266] = true, [29079] = true, [29080] = true, [16259] = true, [16295] = true, [29062] = true, [29064] = true, [29065] = true, [16256] = true, [16281] = true, [16282] = true, [16283] = true, [16284] = true, [16258] = true, [16293] = true, [16181] = true, [16230] = true, [16232] = true, [16233] = true, [16234] = true, [29187] = true, [29189] = true, [29191] = true, [29202] = true, [29205] = true, [29206] = true, [16086] = true, [16544] = true, [16262] = true, [16287] = true, [16182] = true, [16226] = true, [16227] = true, [16228] = true, [16229] = true, [16261] = true, [16290] = true, [16184] = true, [16209] = true, [29192] = true, [29193] = true, [16578] = true, [16579] = true, [16580] = true, [16581] = true, [16582] = true, [16190] = true, [16180] = true, [16196] = true, [16198] = true, [16188] = true, [16268] = true, [16178] = true, [16210] = true, [16211] = true, [16212] = true, [16213] = true, [16187] = true, [16205] = true, [16206] = true, [16207] = true, [16208] = true, [16040] = true, [16113] = true, [16114] = true, [16115] = true, [16116] = true, [16299] = true, [16300] = true, [16301] = true, [28999] = true, [29000] = true, [17364] = true, [16255] = true, [16302] = true, [16303] = true, [16304] = true, [16305] = true, [16179] = true, [16214] = true, [16215] = true, [16216] = true, [16217] = true, [16194] = true, [16218] = true, [16219] = true, [16220] = true, [16221] = true, [16173] = true, [16222] = true, [16223] = true, [16224] = true, [16225] = true, [16252] = true, [16306] = true, [16307] = true, [16308] = true, [16309] = true, [16269] = true, [29082] = true, [29084] = true, [29086] = true, [29087] = true, [29088] = true}
	local Warlock = {[30146] = true, [18788] = true, [30299] = true, [30108] = true, [30283] = true, [30405] = true, [30911] = true, [17803] = true, [32484] = true, [34939] = true, [32394] = true, [18095] = true, [18223] = true, [19028] = true, [18178] = true, [30302] = true, [18288] = true, [17958] = true, [30912] = true, [32385] = true, [32483] = true, [17959] = true, [30404] = true, [18372] = true, [18701] = true, [30292] = true, [23825] = true, [17805] = true, [18265] = true, [18710] = true, [30414] = true, [17810] = true, [27265] = true, [17877] = true, [30296] = true, [18094] = true, [30546] = true, [18938] = true, [18123] = true, [18708] = true, [18136] = true, [18275] = true, [18767] = true, [30301] = true, [32477] = true, [17778] = true, [34935] = true, [35693] = true, [17918] = true, [18756] = true, [18881] = true, [30145] = true, [32383] = true, [17954] = true, [18073] = true, [18135] = true, [18694] = true, [18697] = true, [18707] = true, [23824] = true, [30321] = true, [17782] = true, [17787] = true, [17792] = true, [17814] = true, [17930] = true, [30064] = true, [17788] = true, [17917] = true, [17962] = true, [18182] = true, [18696] = true, [18827] = true, [18871] = true, [17796] = true, [18096] = true, [18174] = true, [18180] = true, [18183] = true, [18213] = true, [18219] = true, [18273] = true, [18744] = true, [27264] = true, [17783] = true, [17815] = true, [18134] = true, [18176] = true, [18179] = true, [18692] = true, [18754] = true, [18755] = true, [18937] = true, [23822] = true, [30326] = true, [17801] = true, [17802] = true, [17836] = true, [17927] = true, [17929] = true, [18220] = true, [18274] = true, [18699] = true, [18704] = true, [18706] = true, [18743] = true, [18770] = true, [18771] = true, [18867] = true, [18868] = true, [18869] = true, [18870] = true, [18930] = true, [32382] = true, [35692] = true, [18119] = true, [18218] = true, [18271] = true, [18695] = true, [18705] = true, [18932] = true, [30288] = true, [30413] = true, [17781] = true, [17786] = true, [17790] = true, [17793] = true, [17812] = true, [17835] = true, [17955] = true, [17956] = true, [17957] = true, [18120] = true, [18126] = true, [18272] = true, [18693] = true, [18698] = true, [18709] = true, [18768] = true, [18769] = true, [18772] = true, [18773] = true, [18821] = true, [18829] = true, [18880] = true, [30144] = true, [30246] = true, [30328] = true, [17779] = true, [17780] = true, [17784] = true, [17785] = true, [17789] = true, [17791] = true, [17804] = true, [17811] = true, [17813] = true, [17833] = true, [17834] = true, [18121] = true, [18122] = true, [18127] = true, [18130] = true, [18131] = true, [18132] = true, [18133] = true, [18177] = true, [18700] = true, [18731] = true, [18879] = true, [18931] = true, [23823] = true, [30060] = true, [30248] = true, [30291] = true, [18175] = true, [18703] = true, [23785] = true, [30143] = true, [30245] = true, [30290] = true, [30057] = true, [30061] = true, [30247] = true, [30293] = true, [30320] = true, [27263] = true, [30295] = true, [35691] = true, [30062] = true, [30063] = true, [30242] = true, [30289] = true, [30319] = true, [32381] = true, [27266] = true, [30054] = true, [30327] = true, [32387] = true, [32392] = true, [32393] = true, [34938] = true}
	local WarlockVan = {[18932] = true, [18938] = true, [18881] = true, [18871] = true, [18931] = true, [18937] = true, [18930] = true, [18870] = true, [18880] = true, [18869] = true, [18879] = true, [18868] = true, [18867] = true, [18119] = true, [18120] = true, [18121] = true, [18122] = true, [18123] = true, [18288] = true, [17788] = true, [17789] = true, [17790] = true, [17791] = true, [17792] = true, [17778] = true, [17779] = true, [17780] = true, [17781] = true, [17782] = true, [17962] = true, [18223] = true, [18220] = true, [18697] = true, [18698] = true, [18699] = true, [18700] = true, [18701] = true, [18788] = true, [17917] = true, [17918] = true, [18130] = true, [18131] = true, [18132] = true, [18133] = true, [18134] = true, [17954] = true, [17955] = true, [17956] = true, [17957] = true, [17958] = true, [17783] = true, [17784] = true, [17785] = true, [17786] = true, [17787] = true, [18708] = true, [18731] = true, [18743] = true, [18744] = true, [18745] = true, [18746] = true, [18751] = true, [18752] = true, [18218] = true, [18219] = true, [17810] = true, [17811] = true, [17812] = true, [17813] = true, [17814] = true, [18827] = true, [18829] = true, [18830] = true, [18310] = true, [18311] = true, [18312] = true, [18313] = true, [18179] = true, [18180] = true, [18181] = true, [17804] = true, [17805] = true, [17806] = true, [17807] = true, [17808] = true, [17864] = true, [18393] = true, [18213] = true, [18372] = true, [18821] = true, [18823] = true, [18824] = true, [18825] = true, [18126] = true, [18127] = true, [18767] = true, [18768] = true, [18703] = true, [18704] = true, [18692] = true, [18693] = true, [17815] = true, [17833] = true, [17834] = true, [17835] = true, [17836] = true, [18694] = true, [18695] = true, [18696] = true, [18182] = true, [18183] = true, [17927] = true, [17929] = true, [17930] = true, [17931] = true, [17932] = true, [17793] = true, [17796] = true, [17801] = true, [17802] = true, [17803] = true, [18774] = true, [18775] = true, [18754] = true, [18755] = true, [18756] = true, [18705] = true, [18706] = true, [18707] = true, [18135] = true, [18136] = true, [23785] = true, [23822] = true, [23823] = true, [23824] = true, [23825] = true, [18709] = true, [18710] = true, [18094] = true, [18095] = true, [18073] = true, [18096] = true, [17959] = true, [18271] = true, [18272] = true, [18273] = true, [18274] = true, [18275] = true, [17877] = true, [18265] = true, [19028] = true, [18174] = true, [18175] = true, [18176] = true, [18177] = true, [18178] = true, [18769] = true, [18770] = true, [18771] = true, [18772] = true, [18773] = true}
	local Warrior = {[29859] = true, [12294] = true, [30356] = true, [30330] = true, [12292] = true, [12328] = true, [13002] = true, [12867] = true, [30033] = true, [20243] = true, [30022] = true, [12975] = true, [12879] = true, [30335] = true, [23881] = true, [12815] = true, [29838] = true, [12704] = true, [16494] = true, [23894] = true, [20505] = true, [29801] = true, [12789] = true, [12330] = true, [12677] = true, [12856] = true, [12974] = true, [23922] = true, [29623] = true, [12701] = true, [12323] = true, [12861] = true, [20496] = true, [23588] = true, [29600] = true, [12281] = true, [12753] = true, [12809] = true, [12838] = true, [29592] = true, [12296] = true, [16462] = true, [12311] = true, [12659] = true, [12664] = true, [23892] = true, [12284] = true, [12958] = true, [13048] = true, [16492] = true, [12666] = true, [12712] = true, [12726] = true, [12814] = true, [12857] = true, [12973] = true, [21552] = true, [12308] = true, [29146] = true, [29836] = true, [12295] = true, [12298] = true, [12322] = true, [12697] = true, [12945] = true, [12960] = true, [35446] = true, [12724] = true, [12781] = true, [12785] = true, [12800] = true, [12834] = true, [20503] = true, [29724] = true, [12287] = true, [12303] = true, [12320] = true, [12725] = true, [12761] = true, [12763] = true, [12783] = true, [12810] = true, [12812] = true, [12813] = true, [12835] = true, [12862] = true, [12961] = true, [12963] = true, [29593] = true, [29721] = true, [12297] = true, [12321] = true, [12752] = true, [12811] = true, [12324] = true, [12727] = true, [16466] = true, [16539] = true, [16540] = true, [16541] = true, [29763] = true, [29776] = true, [29790] = true, [12290] = true, [12299] = true, [12318] = true, [12329] = true, [12765] = true, [12818] = true, [12837] = true, [12849] = true, [12860] = true, [12876] = true, [12959] = true, [12962] = true, [13000] = true, [13045] = true, [21553] = true, [25248] = true, [29140] = true, [29725] = true, [35451] = true, [12282] = true, [12300] = true, [12317] = true, [12663] = true, [12665] = true, [12668] = true, [12676] = true, [12702] = true, [12703] = true, [12713] = true, [12714] = true, [12750] = true, [12751] = true, [12764] = true, [12799] = true, [12803] = true, [12836] = true, [12853] = true, [12855] = true, [12999] = true, [13001] = true, [16493] = true, [16542] = true, [20501] = true, [23584] = true, [23586] = true, [23925] = true, [29595] = true, [29598] = true, [12163] = true, [12285] = true, [12289] = true, [12301] = true, [12313] = true, [12319] = true, [12658] = true, [12700] = true, [12711] = true, [12762] = true, [12788] = true, [12804] = true, [12852] = true, [12858] = true, [12877] = true, [12878] = true, [12950] = true, [12971] = true, [13047] = true, [16487] = true, [23585] = true, [23695] = true, [23893] = true, [29723] = true, [29834] = true, [12286] = true, [12797] = true, [29599] = true, [30016] = true, [30030] = true, [12302] = true, [12312] = true, [12784] = true, [12972] = true, [13046] = true, [16464] = true, [16465] = true, [16489] = true, [16538] = true, [23587] = true, [23924] = true, [25258] = true, [29590] = true, [29760] = true, [29761] = true, [29787] = true, [12807] = true, [16463] = true, [20500] = true, [20504] = true, [25251] = true, [29143] = true, [29762] = true, [29888] = true, [20502] = true, [23923] = true, [29144] = true, [29591] = true, [29792] = true, [29145] = true, [29889] = true, [35449] = true, [35450] = true, [21551] = true, [29594] = true, [29759] = true, [35448] = true}
	local WarriorVan = {[23894] = true, [21553] = true, [23925] = true, [23893] = true, [21552] = true, [23924] = true, [23892] = true, [21551] = true, [23923] = true, [12296] = true, [12297] = true, [12750] = true, [12751] = true, [12752] = true, [12753] = true, [12700] = true, [12781] = true, [12783] = true, [12784] = true, [12785] = true, [16487] = true, [16489] = true, [16492] = true, [23881] = true, [12321] = true, [12835] = true, [12836] = true, [12837] = true, [12838] = true, [12809] = true, [12320] = true, [12852] = true, [12853] = true, [12855] = true, [12856] = true, [12328] = true, [12834] = true, [12849] = true, [12867] = true, [12303] = true, [12788] = true, [12789] = true, [12791] = true, [12792] = true, [16462] = true, [16463] = true, [16464] = true, [16465] = true, [16466] = true, [23584] = true, [23585] = true, [23586] = true, [23587] = true, [23588] = true, [12317] = true, [13045] = true, [13046] = true, [13047] = true, [13048] = true, [12319] = true, [12971] = true, [12972] = true, [12973] = true, [12974] = true, [16493] = true, [16494] = true, [12318] = true, [12857] = true, [12858] = true, [12860] = true, [12861] = true, [20500] = true, [20501] = true, [12301] = true, [12818] = true, [12285] = true, [12697] = true, [12329] = true, [12950] = true, [20496] = true, [12324] = true, [12876] = true, [12877] = true, [12878] = true, [12879] = true, [12313] = true, [12804] = true, [12807] = true, [20502] = true, [20503] = true, [12289] = true, [12668] = true, [23695] = true, [12282] = true, [12663] = true, [12664] = true, [20504] = true, [20505] = true, [12290] = true, [12963] = true, [12286] = true, [12658] = true, [12659] = true, [12797] = true, [12799] = true, [12800] = true, [12311] = true, [12958] = true, [12307] = true, [12944] = true, [12945] = true, [12312] = true, [12803] = true, [12330] = true, [12862] = true, [20497] = true, [20498] = true, [20499] = true, [12308] = true, [12810] = true, [12811] = true, [12302] = true, [12765] = true, [12287] = true, [12665] = true, [12666] = true, [12300] = true, [12959] = true, [12960] = true, [12961] = true, [12962] = true, [12975] = true, [12284] = true, [12701] = true, [12702] = true, [12703] = true, [12704] = true, [12294] = true, [16538] = true, [16539] = true, [16540] = true, [16541] = true, [16542] = true, [12323] = true, [12165] = true, [12830] = true, [12831] = true, [12832] = true, [12833] = true, [23922] = true, [12298] = true, [12724] = true, [12725] = true, [12726] = true, [12727] = true, [12292] = true, [12281] = true, [12812] = true, [12813] = true, [12814] = true, [12815] = true, [12295] = true, [12676] = true, [12677] = true, [12678] = true, [12679] = true, [12299] = true, [12761] = true, [12762] = true, [12763] = true, [12764] = true, [12163] = true, [12711] = true, [12712] = true, [12713] = true, [12714] = true, [12322] = true, [12999] = true, [13000] = true, [13001] = true, [13002] = true}

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
			addPrint("slot="..t..",name="..name..",texture="..iconTexture..",body=")
			addPrint("---")
			addPrint(body)
			addPrint("---")
		end
	end

	addPrint("")
	addPrint("### SPELLS ###")

	local Alchemy = {[28590] = true, [28587] = true, [28588] = true, [28591] = true, [28589] = true, [28586] = true, [28585] = true, [28583] = true, [28584] = true, [28582] = true, [28580] = true, [28581] = true, [47050] = true, [42736] = true, [47046] = true, [47049] = true, [47048] = true, [28578] = true, [28579] = true, [38961] = true, [28575] = true, [28571] = true, [28572] = true, [28577] = true, [28573] = true, [28576] = true, [41458] = true, [41500] = true, [41501] = true, [41502] = true, [41503] = true, [28570] = true, [28565] = true, [28558] = true, [28564] = true, [28563] = true, [28562] = true, [32765] = true, [28566] = true, [28567] = true, [28568] = true, [29688] = true, [28569] = true, [32766] = true, [28557] = true, [28556] = true, [38962] = true, [28555] = true, [38960] = true, [28554] = true, [39639] = true, [28553] = true, [28552] = true, [38070] = true, [28551] = true, [45061] = true, [39637] = true, [39638] = true, [28549] = true, [28550] = true, [33741] = true, [28546] = true, [24266] = true, [28545] = true, [39636] = true, [33733] = true, [28543] = true, [28544] = true, [17632] = true, [33740] = true, [17638] = true, [17636] = true, [17634] = true, [17637] = true, [17635] = true, [33738] = true, [33732] = true, [22732] = true, [25146] = true, [17580] = true, [17577] = true, [17574] = true, [17575] = true, [17576] = true, [17578] = true, [24368] = true, [17573] = true, [24367] = true, [17572] = true, [17571] = true, [17570] = true, [17557] = true, [24366] = true, [24365] = true, [17556] = true, [17559] = true, [17187] = true, [17566] = true, [17561] = true, [17560] = true, [17565] = true, [17563] = true, [17562] = true, [17564] = true, [17555] = true, [17554] = true, [17553] = true, [17552] = true, [3175] = true, [11477] = true, [11478] = true, [26277] = true, [11476] = true, [17551] = true, [11472] = true, [11473] = true, [11468] = true, [11467] = true, [11466] = true, [11461] = true, [11465] = true, [11464] = true, [15833] = true, [11460] = true, [11459] = true, [11479] = true, [11480] = true, [11458] = true, [22808] = true, [4942] = true, [11457] = true, [11452] = true, [11456] = true, [11453] = true, [11448] = true, [11451] = true, [12609] = true, [3454] = true, [3453] = true, [11450] = true, [21923] = true, [7259] = true, [7258] = true, [11449] = true, [3451] = true, [3450] = true, [6618] = true, [7257] = true, [3449] = true, [3448] = true, [3452] = true, [7181] = true, [3188] = true, [6624] = true, [7845] = true, [2333] = true, [7256] = true, [3177] = true, [7837] = true, [3176] = true, [3173] = true, [3174] = true, [3447] = true, [3172] = true, [7255] = true, [7841] = true, [8240] = true, [7179] = true, [3171] = true, [7836] = true, [6617] = true, [2335] = true, [2337] = true, [4508] = true, [3230] = true, [2334] = true, [2332] = true, [2331] = true, [3170] = true, [2329] = true, [7183] = true, [2330] = true, [6619] = true, [2336] = true, [11447] = true, [17579] = true}
	local Engineering = {[46112] = true, [46110] = true, [46113] = true, [46107] = true, [44157] = true, [41307] = true, [30565] = true, [30566] = true, [30575] = true, [30574] = true, [44391] = true, [30556] = true, [46697] = true, [44155] = true, [41315] = true, [41316] = true, [41314] = true, [46108] = true, [41321] = true, [41311] = true, [46115] = true, [46114] = true, [40274] = true, [41312] = true, [46109] = true, [46116] = true, [46106] = true, [41317] = true, [41319] = true, [41318] = true, [46111] = true, [30315] = true, [30334] = true, [30314] = true, [30325] = true, [30332] = true, [41320] = true, [30313] = true, [30563] = true, [30349] = true, [30570] = true, [30318] = true, [30547] = true, [36954] = true, [36955] = true, [30552] = true, [30569] = true, [30316] = true, [30309] = true, [30307] = true, [30308] = true, [30317] = true, [30560] = true, [30329] = true, [39973] = true, [43676] = true, [30347] = true, [30344] = true, [32814] = true, [30341] = true, [39971] = true, [30551] = true, [30311] = true, [30337] = true, [30568] = true, [30348] = true, [30558] = true, [30306] = true, [30312] = true, [30346] = true, [30548] = true, [19831] = true, [19830] = true, [22793] = true, [24356] = true, [24357] = true, [22795] = true, [30310] = true, [22704] = true, [19833] = true, [22797] = true, [23082] = true, [30303] = true, [30304] = true, [30305] = true, [23081] = true, [19825] = true, [19819] = true, [19799] = true, [19815] = true, [19800] = true, [23486] = true, [23489] = true, [19796] = true, [26443] = true, [19814] = true, [19795] = true, [23079] = true, [23080] = true, [39895] = true, [26426] = true, [26427] = true, [26428] = true, [28327] = true, [19794] = true, [23078] = true, [19793] = true, [23096] = true, [23077] = true, [19790] = true, [19792] = true, [19791] = true, [23071] = true, [23129] = true, [26011] = true, [12624] = true, [19567] = true, [23070] = true, [23507] = true, [19788] = true, [12758] = true, [12622] = true, [12621] = true, [12759] = true, [12908] = true, [12620] = true, [12907] = true, [12619] = true, [12754] = true, [12617] = true, [12906] = true, [12618] = true, [12755] = true, [26442] = true, [12905] = true, [8895] = true, [12616] = true, [12615] = true, [26423] = true, [26424] = true, [26425] = true, [12716] = true, [12607] = true, [12614] = true, [12903] = true, [12599] = true, [12603] = true, [12597] = true, [12897] = true, [12902] = true, [12596] = true, [12594] = true, [12899] = true, [12718] = true, [12717] = true, [12595] = true, [12760] = true, [12715] = true, [12895] = true, [15633] = true, [15628] = true, [13240] = true, [3971] = true, [3969] = true, [3972] = true, [15255] = true, [12591] = true, [23069] = true, [3968] = true, [12589] = true, [3967] = true, [21940] = true, [3966] = true, [3965] = true, [8243] = true, [3979] = true, [12587] = true, [3963] = true, [12590] = true, [3962] = true, [26420] = true, [26421] = true, [26422] = true, [12585] = true, [12586] = true, [3961] = true, [3960] = true, [9273] = true, [3959] = true, [3958] = true, [3957] = true, [3955] = true, [3956] = true, [12584] = true, [23067] = true, [23068] = true, [23066] = true, [9271] = true, [3954] = true, [3953] = true, [3952] = true, [3950] = true, [6458] = true, [3949] = true, [9269] = true, [3944] = true, [3942] = true, [26416] = true, [26417] = true, [26418] = true, [3947] = true, [3945] = true, [3946] = true, [3939] = true, [3940] = true, [3941] = true, [3978] = true, [3936] = true, [3938] = true, [3937] = true, [3934] = true, [3933] = true, [8339] = true, [8334] = true, [3973] = true, [3932] = true, [3928] = true, [3931] = true, [3929] = true, [3930] = true, [3926] = true, [3977] = true, [3924] = true, [3925] = true, [7430] = true, [3923] = true, [3922] = true, [3920] = true, [3919] = true, [3918] = true, [30343] = true, [30549] = true, [12719] = true, [12904] = true, [30573] = true, [12720] = true, [12722] = true, [30561] = true, [12900] = true, [30342] = true}
	local Blacksmithing = {[36389] = true, [34542] = true, [36258] = true, [34537] = true, [36261] = true, [36391] = true, [34534] = true, [36257] = true, [41134] = true, [41135] = true, [34548] = true, [34546] = true, [36262] = true, [36256] = true, [38477] = true, [38479] = true, [38478] = true, [34540] = true, [36259] = true, [34544] = true, [36390] = true, [36392] = true, [40034] = true, [40036] = true, [40035] = true, [40033] = true, [36263] = true, [41132] = true, [41133] = true, [34530] = true, [36260] = true, [38473] = true, [38476] = true, [38475] = true, [32657] = true, [29729] = true, [29649] = true, [29645] = true, [29648] = true, [46141] = true, [46144] = true, [46142] = true, [46140] = true, [29669] = true, [29672] = true, [29671] = true, [29699] = true, [29613] = true, [29698] = true, [29694] = true, [29697] = true, [29658] = true, [29621] = true, [29692] = true, [29695] = true, [29617] = true, [29622] = true, [43846] = true, [29700] = true, [29664] = true, [29630] = true, [29693] = true, [29668] = true, [29642] = true, [29643] = true, [42662] = true, [29696] = true, [29662] = true, [29663] = true, [29610] = true, [29619] = true, [29620] = true, [29657] = true, [29616] = true, [29628] = true, [29629] = true, [29608] = true, [29611] = true, [29615] = true, [34533] = true, [34545] = true, [34983] = true, [34535] = true, [29614] = true, [34538] = true, [34543] = true, [34529] = true, [34541] = true, [34547] = true, [32656] = true, [29656] = true, [34608] = true, [32285] = true, [29606] = true, [29728] = true, [29603] = true, [29605] = true, [29571] = true, [42688] = true, [29568] = true, [29569] = true, [36137] = true, [36129] = true, [36136] = true, [36135] = true, [36133] = true, [36134] = true, [36130] = true, [36131] = true, [29566] = true, [29550] = true, [32284] = true, [29556] = true, [29565] = true, [29553] = true, [29558] = true, [29548] = true, [29549] = true, [29552] = true, [29557] = true, [29547] = true, [21161] = true, [16991] = true, [16990] = true, [16994] = true, [23638] = true, [27589] = true, [23639] = true, [23652] = true, [24136] = true, [24138] = true, [24137] = true, [24399] = true, [20897] = true, [23637] = true, [23636] = true, [20876] = true, [20890] = true, [24914] = true, [24912] = true, [24913] = true, [24139] = true, [24140] = true, [24141] = true, [23650] = true, [34982] = true, [16745] = true, [16742] = true, [16744] = true, [20873] = true, [16992] = true, [23633] = true, [16988] = true, [16995] = true, [27585] = true, [23629] = true, [16728] = true, [28244] = true, [28242] = true, [28243] = true, [16663] = true, [16730] = true, [16746] = true, [28463] = true, [28461] = true, [28462] = true, [27586] = true, [27588] = true, [16729] = true, [16993] = true, [23653] = true, [27590] = true, [27830] = true, [16725] = true, [16731] = true, [16665] = true, [16726] = true, [16732] = true, [16664] = true, [27832] = true, [16741] = true, [27587] = true, [16662] = true, [27829] = true, [16724] = true, [29551] = true, [29545] = true, [22757] = true, [32655] = true, [29654] = true, [34607] = true, [20874] = true, [20872] = true, [16657] = true, [16658] = true, [16659] = true, [16661] = true, [16985] = true, [16984] = true, [16660] = true, [16655] = true, [23632] = true, [23628] = true, [16656] = true, [16983] = true, [15296] = true, [16667] = true, [16654] = true, [16978] = true, [16973] = true, [16971] = true, [15295] = true, [16652] = true, [16653] = true, [16970] = true, [16969] = true, [15294] = true, [16651] = true, [20201] = true, [19669] = true, [15293] = true, [16649] = true, [16648] = true, [16650] = true, [15292] = true, [16647] = true, [16646] = true, [10015] = true, [36122] = true, [36125] = true, [36128] = true, [36126] = true, [16645] = true, [36124] = true, [10013] = true, [16644] = true, [10011] = true, [16642] = true, [16643] = true, [16639] = true, [16641] = true, [16640] = true, [10007] = true, [10009] = true, [9979] = true, [9980] = true, [9974] = true, [9970] = true, [10005] = true, [9972] = true, [10003] = true, [9968] = true, [9966] = true, [9964] = true, [10001] = true, [9959] = true, [9961] = true, [9957] = true, [9997] = true, [9952] = true, [9954] = true, [9995] = true, [9950] = true, [9945] = true, [9937] = true, [9939] = true, [9935] = true, [9993] = true, [9933] = true, [9931] = true, [11643] = true, [9928] = true, [9926] = true, [3497] = true, [3515] = true, [11454] = true, [3500] = true, [9916] = true, [34981] = true, [14380] = true, [19668] = true, [9920] = true, [9918] = true, [9921] = true, [3511] = true, [21913] = true, [3503] = true, [15973] = true, [7224] = true, [9820] = true, [7223] = true, [3498] = true, [3513] = true, [9818] = true, [15972] = true, [3508] = true, [3496] = true, [9814] = true, [3505] = true, [3493] = true, [3495] = true, [3507] = true, [3502] = true, [3501] = true, [7222] = true, [9813] = true, [9811] = true, [3504] = true, [3492] = true, [3506] = true, [12259] = true, [3494] = true, [3336] = true, [7221] = true, [14379] = true, [19667] = true, [8768] = true, [3334] = true, [3297] = true, [2675] = true, [6518] = true, [9987] = true, [3333] = true, [9986] = true, [3296] = true, [3331] = true, [2673] = true, [9985] = true, [3295] = true, [3330] = true, [3337] = true, [2674] = true, [3117] = true, [2742] = true, [2672] = true, [2741] = true, [2740] = true, [6517] = true, [3328] = true, [2670] = true, [2668] = true, [3491] = true, [8367] = true, [34979] = true, [7818] = true, [19666] = true, [3292] = true, [7817] = true, [2664] = true, [2667] = true, [3326] = true, [2666] = true, [3294] = true, [7408] = true, [2665] = true, [3116] = true, [3325] = true, [3324] = true, [3323] = true, [3293] = true, [2661] = true, [3321] = true, [43549] = true, [9983] = true, [8880] = true, [2739] = true, [3320] = true, [2738] = true, [3319] = true, [2737] = true, [2662] = true, [2663] = true, [12260] = true, [2660] = true, [3115] = true, [16965] = true, [16986] = true, [16987] = true, [16967] = true, [8366] = true, [8368] = true, [9942] = true, [2671] = true, [16980] = true, [16960] = true}
	local Enchanting = {[27927] = true, [42974] = true, [27984] = true, [27982] = true, [27981] = true, [47051] = true, [32667] = true, [45765] = true, [27954] = true, [27926] = true, [27977] = true, [34008] = true, [34007] = true, [27917] = true, [46594] = true, [33997] = true, [33994] = true, [27924] = true, [27920] = true, [27947] = true, [28004] = true, [28003] = true, [27971] = true, [27914] = true, [34005] = true, [34006] = true, [33999] = true, [34010] = true, [27975] = true, [27972] = true, [32665] = true, [28028] = true, [42620] = true, [46578] = true, [27960] = true, [33992] = true, [27951] = true, [33995] = true, [27946] = true, [27968] = true, [27967] = true, [28019] = true, [27913] = true, [42615] = true, [28022] = true, [27962] = true, [44383] = true, [27911] = true, [27958] = true, [34003] = true, [27945] = true, [34009] = true, [28027] = true, [27950] = true, [27906] = true, [33990] = true, [27905] = true, [27957] = true, [34004] = true, [27961] = true, [33996] = true, [27944] = true, [28016] = true, [27948] = true, [27899] = true, [34001] = true, [33993] = true, [20036] = true, [20035] = true, [34002] = true, [23802] = true, [20011] = true, [20025] = true, [33991] = true, [25086] = true, [25081] = true, [25082] = true, [25083] = true, [25084] = true, [25078] = true, [25074] = true, [25079] = true, [25073] = true, [25080] = true, [25072] = true, [20034] = true, [22750] = true, [20032] = true, [23804] = true, [23803] = true, [22749] = true, [20031] = true, [32664] = true, [25130] = true, [25129] = true, [42613] = true, [20030] = true, [20023] = true, [20010] = true, [20013] = true, [20033] = true, [27837] = true, [23801] = true, [20028] = true, [23800] = true, [23799] = true, [20051] = true, [20015] = true, [20029] = true, [20016] = true, [20024] = true, [20026] = true, [25128] = true, [20009] = true, [20012] = true, [20014] = true, [20017] = true, [13898] = true, [15596] = true, [20020] = true, [20008] = true, [13948] = true, [13947] = true, [25127] = true, [17181] = true, [17180] = true, [13945] = true, [13941] = true, [13943] = true, [13937] = true, [13939] = true, [13935] = true, [13931] = true, [13933] = true, [13917] = true, [13905] = true, [13915] = true, [13890] = true, [13882] = true, [13868] = true, [13887] = true, [13846] = true, [13858] = true, [13836] = true, [13841] = true, [13822] = true, [13815] = true, [13817] = true, [13746] = true, [13794] = true, [13695] = true, [13700] = true, [13698] = true, [13702] = true, [25126] = true, [13689] = true, [13693] = true, [13687] = true, [21931] = true, [13663] = true, [13661] = true, [13659] = true, [13657] = true, [13653] = true, [13655] = true, [14810] = true, [13644] = true, [13646] = true, [13648] = true, [13642] = true, [13637] = true, [13640] = true, [13635] = true, [13631] = true, [14809] = true, [13622] = true, [13626] = true, [13628] = true, [25125] = true, [13529] = true, [13607] = true, [13620] = true, [13617] = true, [13612] = true, [13536] = true, [13538] = true, [13503] = true, [13522] = true, [13501] = true, [13485] = true, [7867] = true, [7863] = true, [7861] = true, [7859] = true, [7857] = true, [13421] = true, [13464] = true, [13380] = true, [13419] = true, [13378] = true, [7793] = true, [7745] = true, [7795] = true, [7786] = true, [7788] = true, [7779] = true, [7782] = true, [7776] = true, [7428] = true, [7771] = true, [14807] = true, [7418] = true, [7766] = true, [7748] = true, [7457] = true, [7454] = true, [25124] = true, [7426] = true, [7443] = true, [7420] = true, [14293] = true, [7421] = true, [28021] = true}
	local Jewelcrafting = {[38503] = true, [38504] = true, [39729] = true, [39705] = true, [39712] = true, [39719] = true, [39741] = true, [39706] = true, [39739] = true, [46777] = true, [46775] = true, [46776] = true, [46779] = true, [46778] = true, [39714] = true, [47053] = true, [39722] = true, [39736] = true, [39731] = true, [39725] = true, [39730] = true, [39733] = true, [39742] = true, [39735] = true, [39717] = true, [39724] = true, [39734] = true, [48789] = true, [47056] = true, [39740] = true, [47055] = true, [39721] = true, [39732] = true, [39711] = true, [39728] = true, [39720] = true, [39715] = true, [39727] = true, [39716] = true, [47054] = true, [39718] = true, [39713] = true, [39710] = true, [39723] = true, [39737] = true, [39738] = true, [31078] = true, [31077] = true, [46601] = true, [46597] = true, [31080] = true, [31079] = true, [31081] = true, [31083] = true, [31082] = true, [46126] = true, [46124] = true, [46127] = true, [46122] = true, [46125] = true, [46123] = true, [31057] = true, [31061] = true, [32867] = true, [32869] = true, [31076] = true, [44794] = true, [41418] = true, [32871] = true, [31072] = true, [32874] = true, [32870] = true, [32872] = true, [32866] = true, [39961] = true, [32873] = true, [32868] = true, [39963] = true, [31070] = true, [31071] = true, [31056] = true, [31062] = true, [31065] = true, [31063] = true, [31066] = true, [31064] = true, [37855] = true, [42592] = true, [42589] = true, [42558] = true, [42593] = true, [42590] = true, [42588] = true, [42591] = true, [31060] = true, [31054] = true, [31055] = true, [31068] = true, [31067] = true, [31053] = true, [39463] = true, [31084] = true, [31089] = true, [31096] = true, [47280] = true, [31112] = true, [31085] = true, [31110] = true, [31091] = true, [46405] = true, [31099] = true, [31109] = true, [31104] = true, [39452] = true, [39462] = true, [31106] = true, [31113] = true, [31108] = true, [31094] = true, [31101] = true, [31107] = true, [41429] = true, [46403] = true, [31111] = true, [46404] = true, [46803] = true, [31098] = true, [31105] = true, [31088] = true, [31103] = true, [31097] = true, [31092] = true, [31102] = true, [31149] = true, [43493] = true, [31095] = true, [31090] = true, [31087] = true, [31100] = true, [39470] = true, [39471] = true, [31058] = true, [40514] = true, [31052] = true, [31051] = true, [41415] = true, [26920] = true, [41414] = true, [39455] = true, [28924] = true, [28907] = true, [39451] = true, [39458] = true, [28957] = true, [28915] = true, [28948] = true, [34069] = true, [28936] = true, [39466] = true, [39467] = true, [38068] = true, [41420] = true, [31050] = true, [26918] = true, [28918] = true, [28914] = true, [28906] = true, [28933] = true, [28955] = true, [28947] = true, [31049] = true, [26916] = true, [31048] = true, [26915] = true, [28905] = true, [34590] = true, [28944] = true, [28917] = true, [28912] = true, [28927] = true, [28953] = true, [26912] = true, [26914] = true, [28938] = true, [28925] = true, [28910] = true, [28916] = true, [28950] = true, [28903] = true, [34961] = true, [26911] = true, [26909] = true, [26910] = true, [34960] = true, [26907] = true, [26908] = true, [26906] = true, [26903] = true, [36526] = true, [26900] = true, [26902] = true, [26896] = true, [26897] = true, [26887] = true, [26885] = true, [26882] = true, [26883] = true, [36525] = true, [26881] = true, [26878] = true, [26880] = true, [32809] = true, [26876] = true, [26875] = true, [26874] = true, [26873] = true, [26872] = true, [34959] = true, [25622] = true, [25621] = true, [34955] = true, [32808] = true, [25620] = true, [25619] = true, [25618] = true, [25617] = true, [25320] = true, [25615] = true, [25613] = true, [25612] = true, [25323] = true, [25321] = true, [25610] = true, [25339] = true, [25498] = true, [32807] = true, [36524] = true, [25318] = true, [25305] = true, [38175] = true, [25317] = true, [36523] = true, [25287] = true, [37818] = true, [25284] = true, [25280] = true, [25490] = true, [26927] = true, [25278] = true, [32801] = true, [25283] = true, [26928] = true, [25493] = true, [26925] = true, [32259] = true, [32178] = true, [32179] = true, [25255] = true, [26926] = true, [32810] = true, [25614] = true}
	local Leatherworking = {[36351] = true, [36349] = true, [36352] = true, [41161] = true, [36355] = true, [39997] = true, [36358] = true, [36357] = true, [41156] = true, [40000] = true, [35576] = true, [35577] = true, [35575] = true, [40001] = true, [36359] = true, [41163] = true, [41164] = true, [36353] = true, [35582] = true, [35584] = true, [35580] = true, [35590] = true, [35591] = true, [35589] = true, [40006] = true, [40005] = true, [40003] = true, [40004] = true, [41157] = true, [41162] = true, [41158] = true, [41160] = true, [40002] = true, [35587] = true, [35588] = true, [35585] = true, [351766] = true, [35538] = true, [351770] = true, [46138] = true, [46137] = true, [46133] = true, [46134] = true, [46136] = true, [46132] = true, [46139] = true, [46135] = true, [35559] = true, [35558] = true, [35567] = true, [35562] = true, [35561] = true, [35564] = true, [35573] = true, [35572] = true, [42731] = true, [35574] = true, [35560] = true, [35563] = true, [35568] = true, [35557] = true, [35554] = true, [35543] = true, [351771] = true, [45117] = true, [42546] = true, [32499] = true, [32500] = true, [32495] = true, [32497] = true, [32496] = true, [35537] = true, [35536] = true, [35535] = true, [35534] = true, [35533] = true, [35532] = true, [35527] = true, [35526] = true, [35525] = true, [32493] = true, [32494] = true, [32498] = true, [35531] = true, [35528] = true, [35529] = true, [32503] = true, [44768] = true, [44359] = true, [32461] = true, [32487] = true, [32488] = true, [32489] = true, [32485] = true, [44770] = true, [44970] = true, [35539] = true, [351769] = true, [35544] = true, [351768] = true, [32490] = true, [32501] = true, [32502] = true, [35524] = true, [35521] = true, [35522] = true, [35523] = true, [35520] = true, [35540] = true, [32465] = true, [32469] = true, [35555] = true, [35549] = true, [36079] = true, [36078] = true, [36077] = true, [32473] = true, [32481] = true, [32468] = true, [32458] = true, [35530] = true, [32457] = true, [32455] = true, [44343] = true, [44344] = true, [32464] = true, [32472] = true, [32480] = true, [32471] = true, [32463] = true, [32467] = true, [32479] = true, [20855] = true, [19107] = true, [19094] = true, [24124] = true, [24125] = true, [24654] = true, [28474] = true, [28473] = true, [28472] = true, [22926] = true, [23708] = true, [22727] = true, [23709] = true, [19097] = true, [24703] = true, [19104] = true, [22921] = true, [23706] = true, [19100] = true, [22927] = true, [28224] = true, [28222] = true, [28223] = true, [23707] = true, [19095] = true, [23710] = true, [20854] = true, [22922] = true, [19093] = true, [28221] = true, [28220] = true, [28219] = true, [24123] = true, [24122] = true, [24121] = true, [19054] = true, [19102] = true, [19091] = true, [19103] = true, [24849] = true, [24851] = true, [24850] = true, [22928] = true, [24846] = true, [24848] = true, [24847] = true, [26279] = true, [22923] = true, [23704] = true, [19101] = true, [19098] = true, [19092] = true, [32456] = true, [32462] = true, [45100] = true, [32466] = true, [32470] = true, [32478] = true, [32482] = true, [32454] = true, [19089] = true, [20853] = true, [19087] = true, [19088] = true, [19090] = true, [19085] = true, [19081] = true, [23705] = true, [19084] = true, [19086] = true, [23703] = true, [19082] = true, [19083] = true, [19077] = true, [19074] = true, [19075] = true, [19078] = true, [19079] = true, [19076] = true, [19080] = true, [44953] = true, [22815] = true, [19073] = true, [24655] = true, [19070] = true, [19072] = true, [19071] = true, [19063] = true, [19066] = true, [19064] = true, [19065] = true, [19067] = true, [19068] = true, [19060] = true, [19062] = true, [19061] = true, [19055] = true, [19059] = true, [19053] = true, [19051] = true, [19052] = true, [36074] = true, [36076] = true, [19050] = true, [19049] = true, [36075] = true, [10650] = true, [19048] = true, [10647] = true, [10632] = true, [10570] = true, [10574] = true, [10572] = true, [19058] = true, [19047] = true, [22331] = true, [10568] = true, [10566] = true, [10562] = true, [10560] = true, [10564] = true, [10558] = true, [10554] = true, [10556] = true, [10630] = true, [10548] = true, [10552] = true, [10619] = true, [14930] = true, [14932] = true, [10542] = true, [10546] = true, [10544] = true, [10621] = true, [10531] = true, [10533] = true, [10525] = true, [10529] = true, [10520] = true, [10516] = true, [10518] = true, [10511] = true, [10507] = true, [10499] = true, [10509] = true, [3779] = true, [10490] = true, [9207] = true, [9208] = true, [10487] = true, [22711] = true, [20650] = true, [10482] = true, [9206] = true, [3777] = true, [6661] = true, [21943] = true, [9202] = true, [7156] = true, [6705] = true, [9201] = true, [3778] = true, [7153] = true, [9198] = true, [3776] = true, [7151] = true, [9196] = true, [9197] = true, [3773] = true, [7149] = true, [3775] = true, [6704] = true, [9195] = true, [4097] = true, [4096] = true, [3774] = true, [7147] = true, [23399] = true, [3772] = true, [3771] = true, [3780] = true, [9194] = true, [9193] = true, [3760] = true, [3818] = true, [20649] = true, [23190] = true, [9149] = true, [3764] = true, [3769] = true, [9148] = true, [9147] = true, [9146] = true, [3770] = true, [3768] = true, [3766] = true, [9145] = true, [3765] = true, [3767] = true, [9074] = true, [9072] = true, [2166] = true, [7135] = true, [7955] = true, [2168] = true, [7954] = true, [7133] = true, [9070] = true, [24940] = true, [2167] = true, [2169] = true, [3762] = true, [3817] = true, [2165] = true, [20648] = true, [9068] = true, [6703] = true, [7953] = true, [2158] = true, [6702] = true, [8322] = true, [3761] = true, [2159] = true, [3763] = true, [3759] = true, [2164] = true, [9065] = true, [2162] = true, [2163] = true, [2161] = true, [3756] = true, [2160] = true, [5244] = true, [9064] = true, [3816] = true, [9060] = true, [9062] = true, [3753] = true, [2153] = true, [2149] = true, [9059] = true, [9058] = true, [7126] = true, [2152] = true, [2881] = true, [10550] = true, [19106] = true}
	local Tailoring = {[31456] = true, [31453] = true, [36315] = true, [36316] = true, [36317] = true, [36318] = true, [41205] = true, [26759] = true, [26758] = true, [31433] = true, [41206] = true, [50194] = true, [40060] = true, [26763] = true, [26762] = true, [31432] = true, [26781] = true, [40021] = true, [40024] = true, [40023] = true, [40020] = true, [26755] = true, [26754] = true, [31455] = true, [31452] = true, [41208] = true, [41207] = true, [31454] = true, [31451] = true, [26784] = true, [37884] = true, [46129] = true, [46131] = true, [46128] = true, [46130] = true, [31444] = true, [26757] = true, [31443] = true, [31450] = true, [26761] = true, [31448] = true, [26780] = true, [26753] = true, [31442] = true, [31449] = true, [26783] = true, [37883] = true, [26777] = true, [26778] = true, [26756] = true, [26760] = true, [26779] = true, [26752] = true, [26782] = true, [31437] = true, [31435] = true, [37873] = true, [31440] = true, [31438] = true, [37882] = true, [26776] = true, [31434] = true, [31441] = true, [26751] = true, [36686] = true, [31373] = true, [26774] = true, [26750] = true, [31459] = true, [26775] = true, [26773] = true, [26749] = true, [31430] = true, [26772] = true, [31431] = true, [26771] = true, [26747] = true, [26770] = true, [26746] = true, [26765] = true, [26764] = true, [22759] = true, [23665] = true, [22866] = true, [27660] = true, [24093] = true, [24092] = true, [24091] = true, [18455] = true, [22870] = true, [26087] = true, [22867] = true, [18451] = true, [18453] = true, [20849] = true, [23667] = true, [20848] = true, [23666] = true, [28210] = true, [28208] = true, [28205] = true, [28207] = true, [28209] = true, [18454] = true, [22868] = true, [23663] = true, [18445] = true, [18452] = true, [22869] = true, [22902] = true, [18448] = true, [18447] = true, [18457] = true, [18458] = true, [18449] = true, [24902] = true, [24903] = true, [24901] = true, [27725] = true, [28481] = true, [28482] = true, [28480] = true, [18456] = true, [18446] = true, [18450] = true, [26745] = true, [31460] = true, [18444] = true, [23664] = true, [18439] = true, [18442] = true, [18441] = true, [18440] = true, [23662] = true, [19435] = true, [26086] = true, [18437] = true, [18436] = true, [18438] = true, [22813] = true, [18434] = true, [18424] = true, [18423] = true, [18420] = true, [27724] = true, [18418] = true, [18422] = true, [27659] = true, [18419] = true, [18416] = true, [18417] = true, [18421] = true, [18415] = true, [18414] = true, [18412] = true, [18413] = true, [18411] = true, [18410] = true, [18409] = true, [18408] = true, [18405] = true, [18406] = true, [18407] = true, [26085] = true, [18404] = true, [18403] = true, [18402] = true, [18560] = true, [12092] = true, [26403] = true, [26407] = true, [50644] = true, [12093] = true, [49677] = true, [12091] = true, [18401] = true, [44950] = true, [44958] = true, [12088] = true, [12086] = true, [50647] = true, [12089] = true, [12081] = true, [12084] = true, [12082] = true, [12085] = true, [12079] = true, [12078] = true, [12076] = true, [12080] = true, [12077] = true, [12073] = true, [12072] = true, [12074] = true, [12075] = true, [12069] = true, [12067] = true, [12070] = true, [27658] = true, [12065] = true, [12066] = true, [12071] = true, [12064] = true, [12053] = true, [12060] = true, [12056] = true, [12055] = true, [12061] = true, [12059] = true, [12050] = true, [8804] = true, [12052] = true, [12049] = true, [12048] = true, [8802] = true, [3862] = true, [3864] = true, [3873] = true, [8797] = true, [8799] = true, [8795] = true, [8793] = true, [8770] = true, [21945] = true, [6695] = true, [3861] = true, [8791] = true, [3872] = true, [8789] = true, [8774] = true, [3863] = true, [8766] = true, [8786] = true, [3860] = true, [8772] = true, [6693] = true, [8489] = true, [3865] = true, [8764] = true, [3858] = true, [3871] = true, [3857] = true, [8784] = true, [8762] = true, [8483] = true, [3870] = true, [3859] = true, [6692] = true, [3813] = true, [8782] = true, [3854] = true, [8780] = true, [8760] = true, [8758] = true, [3856] = true, [6690] = true, [3869] = true, [3852] = true, [3868] = true, [3851] = true, [3855] = true, [3839] = true, [12047] = true, [3849] = true, [7892] = true, [7893] = true, [7643] = true, [6688] = true, [3848] = true, [3850] = true, [3866] = true, [8467] = true, [2403] = true, [7639] = true, [3844] = true, [2406] = true, [3758] = true, [3847] = true, [2401] = true, [6521] = true, [2399] = true, [3843] = true, [3845] = true, [3757] = true, [12046] = true, [2402] = true, [2964] = true, [2395] = true, [7633] = true, [2396] = true, [3842] = true, [6686] = true, [2386] = true, [3841] = true, [2397] = true, [7630] = true, [7629] = true, [3755] = true, [2394] = true, [2389] = true, [2392] = true, [8465] = true, [3840] = true, [3914] = true, [7623] = true, [7624] = true, [12045] = true, [8776] = true, [2385] = true, [3915] = true, [2387] = true, [12044] = true, [2393] = true, [2963] = true, [8778] = true, [7636] = true, [31461] = true, [36670] = true, [36672] = true, [36669] = true, [36667] = true, [36668] = true, [36665] = true, [12090] = true, [12063] = true, [12083] = true, [12062] = true, [12087] = true, [12068] = true}
	local Cooking = {[42302] = true, [42305] = true, [33296] = true, [38868] = true, [38867] = true, [42296] = true, [33295] = true, [33287] = true, [33289] = true, [33288] = true, [43707] = true, [43765] = true, [45022] = true, [33293] = true, [33294] = true, [33286] = true, [33292] = true, [33285] = true, [43772] = true, [25659] = true, [33290] = true, [43761] = true, [33279] = true, [36210] = true, [33291] = true, [33284] = true, [43758] = true, [24801] = true, [18247] = true, [18245] = true, [18246] = true, [22761] = true, [46684] = true, [46688] = true, [18243] = true, [18244] = true, [18240] = true, [18242] = true, [18239] = true, [18241] = true, [15933] = true, [15915] = true, [18238] = true, [22480] = true, [20626] = true, [15906] = true, [15910] = true, [21175] = true, [4094] = true, [15863] = true, [7213] = true, [15856] = true, [15861] = true, [20916] = true, [15865] = true, [15855] = true, [25954] = true, [3400] = true, [7828] = true, [13028] = true, [3399] = true, [24418] = true, [3376] = true, [3398] = true, [6500] = true, [15853] = true, [3373] = true, [3397] = true, [3377] = true, [6419] = true, [2548] = true, [7755] = true, [6418] = true, [2549] = true, [2547] = true, [45695] = true, [6501] = true, [6417] = true, [3372] = true, [2545] = true, [8238] = true, [3370] = true, [2546] = true, [25704] = true, [2544] = true, [2543] = true, [3371] = true, [28267] = true, [9513] = true, [33278] = true, [6499] = true, [2541] = true, [6415] = true, [2542] = true, [7754] = true, [7753] = true, [7827] = true, [6416] = true, [8607] = true, [21144] = true, [6414] = true, [2795] = true, [6413] = true, [6412] = true, [2539] = true, [43779] = true, [7751] = true, [15935] = true, [21143] = true, [8604] = true, [33276] = true, [33277] = true, [7752] = true, [37836] = true, [2538] = true, [2540] = true, [818] = true}
	local FirstAid = {[27033] = true, [27032] = true, [23787] = true, [18630] = true, [18629] = true, [10841] = true, [10840] = true, [7929] = true, [7928] = true, [7935] = true, [3278] = true, [7934] = true, [3277] = true, [3276] = true, [3275] = true, [30021] = true}

	for i = 1, GetNumSpellTabs() do
		local _, _, offset, numSlots = GetSpellTabInfo(i)
		for j = offset+1, offset+numSlots do
			local spellType, spellID = GetSpellBookItemInfo(j, BOOKTYPE_SPELL)
			if (Druid[spellID] or Hunter[spellID] or Mage[spellID] or Paladin[spellID] or Priest[spellID] or Rogue[spellID] or Shaman[spellID] or Warlock[spellID] or Warrior[spellID]
				or DruidVan[spellID] or HunterVan[spellID] or MageVan[spellID] or PaladinVan[spellID] or PriestVan[spellID] or RogueVan[spellID] or ShamanVan[spellID] or WarlockVan[spellID] or WarriorVan[spellID]
				or Alchemy[spellID] or Engineering[spellID] or Blacksmithing[spellID] or Enchanting[spellID] or Jewelcrafting[spellID] or Leatherworking[spellID] or Tailoring [spellID]
				or Cooking[spellID] or FirstAid[spellID]) then
				--Skip because we'll manually add talent and profession spells later
			else
				addPrint(spellID)
			end
		end
	end
	-- Add Talent spells
	tab = {}
	vanTab = {}
	if (pclass == "druid") then
		tab = Druid
		vanTab = DruidVan
	elseif (pclass == "hunter") then
		tab = Hunter
		vanTab = HunterVan
	elseif (pclass == "mage") then
		tab = Mage
		vanTab = MageVan
	elseif (pclass == "paladin") then
		tab = Paladin
		vanTab = PaladinVan
	elseif (pclass == "priest") then
		tab = Priest
		vanTab = PriestVan
	elseif (pclass == "rogue") then
		tab = Rogue
		vanTab = RogueVan
	elseif (pclass == "shaman") then
		tab = Shaman
		vanTab = ShamanVan
	elseif (pclass == "warlock") then
		tab = Warlock
		vanTab = WarlockVan
	elseif (pclass == "warrior") then
		tab = Warrior
		vanTab = WarriorVan
	end
	-- Talents
	for k,_ in pairs(tab) do
		if (IsPlayerSpell(k)) then
			vanTab[k] = false
			addPrint(k)
		end
	end
	for k,b in pairs(vanTab) do
		if (b and IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	--Professions
	for k,_ in pairs(Engineering) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(Blacksmithing) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(Enchanting) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(Jewelcrafting) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(Leatherworking) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(Tailoring) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(Cooking) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
		end
	end
	for k,_ in pairs(FirstAid) do
		if (IsPlayerSpell(k)) then
			addPrint(k)
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

	addPrint("")
	addPrint("### EOF ###")

	-- show the appropriate frames
	
	--SimcCopyFrame:Show()
	--SimcCopyFrameScroll:Show()
	--SimcCopyFrameScrollText:Show()
	--SimcCopyFrameScrollText:SetText(QEProfile)
	--SimcCopyFrameScrollText:HighlightText()
	--SimcCopyFrameScrollText:SetScript("OnEscapePressed", function(self)
    --SimcCopyFrame:Hide()
  --end)
	--SimcCopyFrameButton:SetScript("OnClick", function(self)
    --SimcCopyFrame:Hide()
  --end)
  
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
    f:SetMinResize(150, 100)
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
	QEProfile = QEProfile .. line .. "\n";
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

function checkIfUsable(classID, subclassID) 
	_, pclass = UnitClass("player")
	
	--armorTypes = {
	--	["Priest"] = [0, 1],
	--	["Druid"] = [0, 1, 2, 8],
	--	["Shaman"] = [0, 1, 2, 3, 6, 9],
	--	["Paladin"] = [0, 1, 2, 3, 4, 6, 7]
	--}
		
	classArmor = {
		["Priest"] = 1,
		["Mage"] = 1,
		["Warlock"] = 1,
		["Rogue"] = 2,
		["Druid"] = 2,
		["Shaman"] = 3,
		["Hunter"] = 3,
		["Paladin"] = 4,
		["Warrior"] = 4
	}
	
	classWeps = {
		["Rogue"] = "OneHanded Axes, OneHanded Daggers, OneHanded Maces",
		["Druid"] = "OneHanded Maces, TwoHanded Maces, Staves, Fist Weapons, OneHanded Dagger",
		["Paladin"] = "OneHanded Maces, TwoHanded Maces, OneHanded Axes, TwoHanded Axes, OneHandedSwords, TwoHandedSwords, Polearms",
		["Priest"] = "OneHanded Maces, OneHanded Daggers, Staves",
		["Mage"] = "OneHanded Dagger, OneHanded Sword, Staves, Wands",
		["Warlock"] = "",
		["Shaman"] = "",
		["Hunter"] = "",
		["Warrior"] = ""
	}
		
		
	--print(itemType .. "/" .. pclass .. "/" .. armorTypes[subType] .. "/" .. classArmor[pclass]) 
	--print(itemType)
	--print(subType)
	--print(armorTypes[subType])
	
	if (classID == 4) then
	
		armorType = armorTypes[pclass]
		--classType = classArmor[pclass]
		
		return armorType
		
	elseif (classID == 2) then
	
		stype = subType:gsub('%-', '')
		--print(string.find(classWeps[pclass], stype))
	
		return string.find(classWeps[pclass], stype)
	
	end
end


SLASH_QE1 = "/qe";
SlashCmdList["QE"] = scanGear;

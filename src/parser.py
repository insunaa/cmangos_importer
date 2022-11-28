from datetime import datetime
import datetime
import time
import math
from src.constants import *


def clean(mystr, chars_to_remove=("\n",)):
    return "".join([e for e in mystr if e not in chars_to_remove])


def parse_file(f, exp):
    def get_char_info():
        global skills
        char = f[3].split("=")
        char_class = char[0]
        char_race = clean(f[5].split("=")[1])
        armor_skill = skillmap[char_class]["armor"]
        weapon_skills = skillmap[char_class]["weapons"]

        result = dict(
            char_name=clean(char[1], ["\n", '"']),
            char_gender=clean(f[6].split("=")[1]),
            char_class=classes[char_class],
            char_race=races[char_race],
            char_level=clean(f[4].split("=")[1]),
            char_expansion=clean(f[13].split("=")[1]),
            char_health=10000,
            char_power=0,
        )

        if len(armor_skill):
            skills += skillsTemplate.fill(
                skill_id=armor_skill[0],
                current_skill=1,
                max_skill=1,
            )
        for weaponSkill in weapon_skills:
            skills += skillsTemplate.fill(
                skill_id=weaponSkill,
                current_skill=int(result["char_level"]) * 5,
                max_skill=int(result["char_level"]) * 5,
            )

        exp =  clean(f[13].split("=")[1])

        return result

    def add_to_itemlists(slot_id, item_entry, suffix, enchant, gems, bag_id=0, item_count=1):
        global inventory_list, instance_list, itemguiditr
        socketBonus = 0
        inventory_list += wornTemplate.fill(
            slot_id=slot_id,
            item_guid=itemguiditr,
            item_entry=item_entry,
            bag_id=bag_id,
        )
        sockets = [gems[0].split(":")[1], gems[1].split(":")[1], gems[2].split(":")[1]]
        suffix = abs(int(suffix))
        enchantments = ""
        if exp == 0:
            suffix = 0
            enchantments = instanceEnchantTemplateVan.fill(
                main_enchant=enchant,
                enchant_1=suffixTable[str(suffix)][0],
                enchant_2 = suffixTable[str(suffix)][0],
                enchant_3 = suffixTable[str(suffix)][0]
                )
        elif exp == 1:
            if "false" not in sockets and "true" in sockets:
                socketBonus = itemSocketBonusMap[int(item_entry)]
            if str(suffix) not in suffixTable:
                suffix = 0
            enchantments = instanceEnchantTemplateTBC.fill(
                main_enchant=enchant,
                gem1=gemPropertyMap[gemIDPropertyMap[int(gems[0].split(":")[0])]],
                gem2=gemPropertyMap[gemIDPropertyMap[int(gems[1].split(":")[0])]],
                gem3=gemPropertyMap[gemIDPropertyMap[int(gems[2].split(":")[0])]],
                socket_bonus=socketBonus,
                enchant_1=suffixTable[str(suffix)][0],
                enchant_2=suffixTable[str(suffix)][1],
                enchant_3=suffixTable[str(suffix)][2],
                )
        elif exp == 2:
            if "false" not in sockets and "true" in sockets and int(item_entry) in itemSocketBonusMapWotlk:
                socketBonus = itemSocketBonusMapWotlk[int(item_entry)]
            if str(suffix) not in suffixTable:
                suffix = 0
            enchantments = instanceEnchantTemplateWOTLK.fill(
                main_enchant=enchant,
                gem1=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gems[0].split(":")[0])]],
                gem2=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gems[1].split(":")[0])]],
                gem3=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gems[2].split(":")[0])]],
                socket_bonus=socketBonus,
                enchant_1=suffixTable[str(suffix)][0],
                enchant_2=suffixTable[str(suffix)][1],
                enchant_3=suffixTable[str(suffix)][2],
                )
        if exp != 2:
            instance_list += instanceTemplate.fill(
                item_guid=itemguiditr,
                item_entry=item_entry,
                item_count=item_count,
                item_suffix=-suffix,
                enchantments=enchantments,
            )
            itemguiditr += 2
        else:
            instance_list += instanceTemplateWotLK.fill(
                item_guid=itemguiditr,
                item_entry=item_entry,
                item_count=item_count,
                item_suffix=-suffix,
                enchantments=enchantments,
            )
            itemguiditr += 2

    def parse_slots_equipped():
        def parse_slots_base():
            item_info = f[i + equip_offset].split(",")
            suffix = "0"
            enchant = "0"
            gems = []
            if len(item_info) == 8:
                suffix = item_info[2].split("=")[1]
                enchant = item_info[4].split("=")[1]
                gems = [item_info[5].split("=")[1], item_info[6].split("=")[1], item_info[7].split("=")[1]]
            elif len(item_info) == 6:
                enchant = item_info[2].split("=")[1]
                gems = [item_info[3].split("=")[1], item_info[4].split("=")[1], item_info[5].split("=")[1]]

            item_entry = (
                f[i + equip_offset].split("=")[2].split(",")[0].replace("\n", "")
            )
            add_to_itemlists(slotMap[slot], item_entry, suffix, enchant, gems)

        slots = [
            "head",
            "neck",
            "shoulder",
            "chest",
            "waist",
            "legs",
            "feet",
            "wrist",
            "hands",
            "finger1",
            "finger2",
            "trinket1",
            "trinket2",
            "back",
            "main_hand",
            "off_hand",
            "relic",
            "tabard",
        ]

        for slot in slots:
            for i in range(19):
                if slot not in (f[i + equip_offset]):
                    continue
                parse_slots_base()

    def parse_pet():
        if char_info["char_class"] != classes["hunter"]:
            return
        global pet_list
        petFamily = 0
        petHealth = 30000
        petPower = 100
        modelId = 706
        for i in range(equip_offset, 40):
            if "pet" in f[i]:
                petInfo = f[i].split(",")
                petName = clean(petInfo[0].split("=")[1])
                petLevel = clean(petInfo[1].split("=")[1])
                petEntry = clean(petInfo[2].split("=")[1])
                if len(petInfo) == 6:
                    petFamily = clean(petInfo[3].split("=")[1])
                    modelId = genericPetModelMap[petFamily]
                    petHealth = clean(petInfo[4].split("=")[1])
                    petPower = clean(petInfo[5].split("=")[1])
                pet_list = petTemplate.fill(
                    no_char_guid=True,
                    pet_entry=petEntry,
                    pet_owner=char_guid,
                    pet_name=petName,
                    pet_level=petLevel,
                    pet_model=modelId,
                    pet_health=petHealth,
                    pet_resource=petPower,
                )
                break

    def get_all_items():
        all_items = dict(
            # [header, start, end, file lines]
            gear=["GEAR FROM BAG", 0, 0, []],
            talents=["TALENTS", 0, 0, []],
            actions=["ACTIONS", 0, 0, []],
            macros=["MACROS", 0, 0, []],
            spells=["SPELLS", 0, 0, []],
            factions=["FACTIONS", 0, 0, []],
            glyphs=["GLYPHS", 0, 0, []],
            achievements=["ACHIEVEMENTS", 0, len(f), []],
        )
        previous_k = ""
        for k, v in all_items.items():
            for line in f:
                all_items[k][1] += 1
                if v[0] in line:
                    if previous_k:
                        all_items[previous_k][2] = all_items[k][1]
                    previous_k = k
                    break
        for k, v in all_items.items():
            for i in range(v[1], v[2] -1):
                text = f[i].rstrip("\n")
                if text:
                    v[3].append(text)

        return all_items

    def parse_bag(all_items):
        def parse_bag_base():
            nonlocal firstSlot, bagID
            suffix = "0"
            enchant = "0"
            gems = []
            item_data = item.split(",")
            item_count = ""
            item_entry = item_data[0].split("=")
            if len(item_entry) > 1:
                item_entry = item_entry[1]
            if len(item_data) > 1:
                item_count = clean(item_data[1].split("=")[1])
            if len(item_data) == 8:
                item_count = clean(item_data[3].split("=")[1])
                suffix = item_data[1].split("=")[1]
                enchant = item_data[4].split("=")[1]
                gems = [item_data[5].split("=")[1], item_data[6].split("=")[1], item_data[7].split("=")[1]]
            if len(item_data) == 6:
                enchant = item_data[2].split("=")[1]
                gems = [item_data[3].split("=")[1], item_data[4].split("=")[1], item_data[5].split("=")[1]]
            slotID = firstSlot % 28
            bagID = int(firstSlot / 28) + 216
            add_to_itemlists(slotID, item_entry, suffix, enchant, gems, bagID, item_count=item_count)
            firstSlot += 1

        firstSlot = 23 + 14
        bagID = 1
        for item in all_items["gear"][3]:
            parse_bag_base()

    def parse_spells(all_items):
        global skills, spells, action_list, faction_list, talents
        if exp > 0 and str(34093) not in all_items["spells"][3]:
            spells += spellTemplate.fill(spell_id=34093)
        for spell in all_items["spells"][3]:
            spell = int(spell)
            if spell == 348700:
                spell = 31892
            if spell == 348704:
                spell = 31801
            spells += spellTemplate.fill(spell_id=spell)
            for index in range(len(talentArray)):
                talent = talentArray[index]
                if int(talent["r0"]) == spell:
                    talents+=talentTemplate.fill(talent_id=talent["id"],current_rank=0)
                elif int(talent["r1"]) == spell:
                    talents+=talentTemplate.fill(talent_id=talent["id"],current_rank=1)
                elif int(talent["r2"]) == spell:
                    talents+=talentTemplate.fill(talent_id=talent["id"],current_rank=2)
                elif int(talent["r3"]) == spell:
                    talents+=talentTemplate.fill(talent_id=talent["id"],current_rank=3)
                elif int(talent["r4"]) == spell:
                    talents+=talentTemplate.fill(talent_id=talent["id"],current_rank=4)

        professions_spells = [
            int(e) for e in all_items["spells"][3] if int(e) in all_prof_skill_ids
        ]
        for spell in professions_spells:
            for profession in professionMap:
                if learned_professions[profession]:
                    continue
                if int(spell) in professionMap[profession]:
                    learned_professions[profession] = True
                    skills += skillsTemplate.fill(
                        skill_id=professionSkillMap[profession],
                        current_skill=maxSkillMap["professions"][exp],
                        max_skill=maxSkillMap["professions"][exp],
                    )
                    if (
                        str(professionSpellMap[exp][profession])
                        not in all_items["spells"][3]
                    ):
                        # override what player has and give him top profession level
                        spells += spellTemplate.fill(
                            spell_id=professionSpellMap[exp][profession]
                        )

        for action in all_items["actions"][3]:
            actionInfo = action.split(",")
            slot = actionInfo[0].split("=")[1]
            actiontype = actionInfo[1].split("=")[1]
            actionId = actionInfo[2].split("=")[1].replace("\n", "")
            slot = int(slot) - 1
            if exp != 2:
                action_list += actionTemplate.fill(
                    slot_id=slot,
                    action_id=actionId,
                    action_type=actionMap[actiontype],
                )
            else:
                action_list += actionTemplateWotLK.fill(
                    slot_id=slot,
                    action_id=actionId,
                    action_type=actionMap[actiontype],
                )

        for faction in all_items["factions"][3]:
            factionInfo = faction.split(",")
            factionId = factionInfo[0]
            factionStanding = factionInfo[1]
            faction_list += factionTemplate.fill(
                faction_id=factionId,
                faction_standing=factionStanding,
            )

    def parse_macros():
        macroArrayArray = []
        miniMacroArray = []
        macroCounter = 0
        macroMeta = {}
        for macro in all_items["macros"][3]:
            if len(macro.split(",")) > 1:
                macroInfo = macro.split(",")
                if "slot" in macroInfo[0]:
                    macroSlot = macroInfo[0].split("=")[1]
                    macroName = macroInfo[1].split("=")[1]
                    macroTexture = macroInfo[2].split("=")[1]
                    macroMeta[macroSlot] = [macroName, macroTexture]
        for macro in all_items["macros"][3]:
            if ("---" in macro) and (macroCounter == 0):
                macroCounter += 1
                continue
            if ("---" in macro) and (macroCounter > 0):
                macroArrayArray.append(miniMacroArray)
                miniMacroArray = []
                macroCounter = 0
                continue
            if macroCounter > 0:
                miniMacroArray.append(macro.replace("\n", "").replace("@", "target="))
                macroCounter += 1
                continue
        i = 0
        for metaMacro in macroMeta:
            macroMeta[metaMacro].append(macroArrayArray[i])
            i += 1

        macroBodies = ""

        for macroSlot in macroMeta:
            if (int(macroSlot) < 100):
                continue
            fullMacro = macroMeta[macroSlot]
            macroBody = ""
            for bodyPart in fullMacro[2]:
                macroBody += bodyPart + "\n"
            macroBody = macroBody.rstrip("\n")
            actualBody = singleMacroTemplate.fill(
                macro_guid=16777216 + int(macroSlot) - 120,
                macro_body=macroBody,
                macro_name=fullMacro[0],
            )
            macroBodies += actualBody
        write_macros(macroBodies)
    
    def parse_glyphs():
        global glyphs
        for glyph in all_items["glyphs"][3]:
            glyphslot = int(glyph.split(",")[0])
            glyphspell = glyph.split(",")[1]
            if glyphspell in glyphMap:
                glyphs += glyphTemplate.fill(glyph_slot=glyphslot-1,glyph_id=glyphMap[glyphspell])

    def parse_achievements():
        global achievements
        for achievement in all_items["achievements"][3]:
            achId = achievement.split(",")[0]
            year = int(achievement.split(",")[1])
            month = int(achievement.split(",")[2])
            day = int(achievement.split(",")[3])
            date_time = datetime.datetime(year+2000, month, day, 0, 0)
            timestamp = time.mktime(date_time.timetuple())
            achievements += achievementTemplate.fill(achievement_id=achId,timestamp=timestamp)

    def write_pdump(char_info):
        startPos = startPosMap[exp][factions[clean(f[5].split("=")[1])]]
        version = ""
        charactersRow = ""
        enchantments = ""
        textIns = ""
        bagId = 23162
        if exp == 0:
            version = "required_z2799_01_characters_account_data"
            enchantments = instanceEnchantTemplateVan.fill(main_enchant=0, enchant_1=0, enchant_2=0, enchant_3=0)
            bagId = 14156
            charactersRow = charactersTemplateVan.fill(
                **char_info,
                pos_x=startPos[0],
                pos_y=startPos[1],
                pos_z=startPos[2],
                start_map=startPos[3])
        elif exp == 1:
            version = "required_s2452_01_characters_fishingSteps"
            enchantments = instanceEnchantTemplateTBC.fill(main_enchant=0, gem1=0, gem2=0, gem3=0, socket_bonus=0, enchant_1=0, enchant_2=0, enchant_3=0)
            charactersRow = charactersTemplateTBC.fill(
                **char_info,
                pos_x=startPos[0],
                pos_y=startPos[1],
                pos_z=startPos[2],
                start_map=startPos[3])
        else:
            version = "required_14061_01_characters_fishingSteps"
            enchantments = instanceEnchantTemplateWOTLK.fill(main_enchant=0, gem1=0, gem2=0, gem3=0, socket_bonus=0, enchant_1=0, enchant_2=0, enchant_3=0)
            charactersRow = charactersTemplateWOTLK.fill(
                **char_info,
                pos_x=startPos[0],
                pos_y=startPos[1],
                pos_z=startPos[2],
                start_map=startPos[3])
            textIns=", ''"

        result = pdumpTemplate.fill(
            bag_id=bagId,
            characters_row=charactersRow,
            enchantments=enchantments,
            database_version=version,
            pos_x=startPos[0],
            pos_y=startPos[1],
            pos_z=startPos[2],
            start_map=startPos[3],
            skills=skills,
            actions=action_list,
            inventory_list=inventory_list,
            pet_list=pet_list,
            spells=spells,
            talents=talents,
            instance_list=instance_list,
            factions=faction_list,
            text=textIns,
            glyphs=glyphs,
            achievements=achievements,
        )

        randNo = datetime.datetime.now().strftime("%H%M%S")

        with open(char_info["char_name"] + randNo + ".sql", "w") as writer:
            writer.write(result)
            print("Character conversion successful! Export written to: " + char_info["char_name"] + randNo + ".sql")

    def write_macros(macro_file):
        with open("macros-cache.txt", "w") as writer:
            writer.write(macro_file)

    char_info = get_char_info()
    parse_slots_equipped()
    parse_pet()
    all_items = get_all_items()
    parse_bag(all_items)
    parse_spells(all_items)
    parse_macros()
    parse_glyphs()
    parse_achievements()
    write_pdump(char_info)
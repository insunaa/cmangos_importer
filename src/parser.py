
from random import random
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

        return result

    def add_to_itemlists(slot_id, item_entry, suffix, bag_id=0,item_count=1):
        global inventory_list, instance_list, itemguiditr
        inventory_list += wornTemplate.fill(
            slot_id=slot_id,
            item_guid=itemguiditr,
            item_entry=item_entry,
            bag_id=bag_id,
        )
        instance_list += instanceTemplate.fill(
            item_guid=itemguiditr,
            item_entry=item_entry,
            item_count=item_count,
            item_suffix=-int(suffix),
            enchant_1=suffixTable[suffix][0],
            enchant_2=suffixTable[suffix][1],
            enchant_3=suffixTable[suffix][2],
        )
        itemguiditr += 2

    def parse_slots_equipped():
        def parse_slots_base():
            item_info = f[i + equip_offset].split(",")
            suffix = "0"
            if len(item_info) == 4:
                suffix = item_info[2].split("=")[1]
            item_entry = (
                f[i + equip_offset].split("=")[2].split(",")[0].replace("\n", "")
            )
            add_to_itemlists(slotMap[slot], item_entry, suffix)

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
        modelId = 18923
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
            factions=["FACTIONS", 0, len(f), []],
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
            item_data = item.split(",")
            item_count = ""
            item_entry = item_data[0].split("=")
            if len(item_entry) > 1:
                item_entry = item_entry[1]
            if len(item_data) > 1:
                item_count = clean(item_data[1].split("=")[1])
            if len(item_data) == 4:
                item_count = clean(item_data[3].split("=")[1])
                suffix = item_data[1].split("=")[1]
            slotID = firstSlot % 28
            bagID = int(firstSlot / 28) + 216
            add_to_itemlists(slotID, item_entry, suffix, bagID,item_count=item_count)
            firstSlot += 1

        firstSlot = 23 + 14
        bagID = 1
        for item in all_items["gear"][3]:
            parse_bag_base()

    def parse_spells(all_items):
        global skills, spells, action_list, faction_list
        if exp > 0 and str(34093) not in all_items["spells"][3]:
            spells += spellTemplate.fill(spell_id=34093)
        for spell in all_items["spells"][3]:
            spell = int(spell)
            if spell == 348700:
                spell = 31892
            if spell == 348704:
                spell = 31801
            spells += spellTemplate.fill(spell_id=spell)

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
            action_list += actionTemplate.fill(
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
                miniMacroArray.append(macro.replace("\n", ""))
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

    def write_pdump(char_info):
        result = pdumpTemplate.fill(
            **char_info,
            skills=skills,
            actions=action_list,
            inventory_list=inventory_list,
            pet_list=pet_list,
            spells=spells,
            instance_list=instance_list,
            factions=faction_list,
        )

        randNo = str(int(random()*10000))

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
    write_pdump(char_info)
#!/usr/bin/python3

"""
Author: insuna
Copyright © 2022, insuna All rights reserved
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    (1) Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer. 

    (2) Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.  
    
    (3)The name of the author may not be used to
    endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE. """

from string import Template
import sys
import os.path

pdumpTemplate = Template("""IMPORTANT NOTE: This sql queries not created for apply directly, use '.pdump load' command in console or client chat instead.
IMPORTANT NOTE: NOT APPLY ITS DIRECTLY to character DB or you will DAMAGE and CORRUPT character DB

UPDATE character_db_version SET required_s2429_01_characters_raf = 1 WHERE FALSE;

INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '70', '0', '300000000', '0', '0', '65568', '-1817.69', '5321.56', '-12.4282', '530', '0', '1.86449', '2 0 0 8 0 0 1048576 0 0 0 0 0 0 0 0 0 ', '0', '1', '200', '175', '1642414101', '1', '0', '0', '0', '0', '0', '0', '0', '0', '10', '0', '0', '3703', '0', '', '0', '0', '0', '0', '0', '0', '0', '0', '2147483647', '0', '5594', '0', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', NULL, '0', '0 0 ', '0', '0', NULL, NULL, NULL);
INSERT INTO `character_homebind` VALUES ('$char_guid', '530', '3703', '-1817.69', '5321.56', '-12.4282');
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '24', '184', '6948'); -- Hearthstone
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '19', '217', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '22', '218', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '21', '219', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '20', '220', '23162'); -- Large Bag
$inventory_list$pets
$skills
$spells
INSERT INTO `item_instance` VALUES ('184', '$char_guid', '6948', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('217', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('218', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('219', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('220', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
$instance_list
$actions
$factions
$macros
""")

skillsTemplate = Template("""INSERT INTO `character_skills` VALUES ('$char_guid', '$skill_id', '$current_skill', '$max_skill');
""")

wornTemplate = Template("""INSERT INTO `character_inventory` VALUES ('$char_guid', '$bag_id', '$slot_id', '$item_guid', '$item_entry');
""")

instanceTemplate = Template("""INSERT INTO `item_instance` VALUES ('$item_guid', '$char_guid', '$item_entry', '0', '0', '$item_count', '0', '-1 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 0 0 0 ', '$item_suffix', '100', '0');
""")

actionTemplate = Template("INSERT INTO `character_action` VALUES ('$char_guid', '$slot_id', '$action_id', '$action_type');\n")

petTemplate = Template("\nINSERT INTO `character_pet` VALUES ('10000', '$pet_entry', '$pet_owner', '$pet_model', '13481', '1', '70', '0', '1', '1000', '6', '0', '300', '$pet_name', '1', '0', '$pet_health', '$pet_resource', '157750', '1642440972', '0', '0', '7 2 7 1 7 0 129 0 129 0 129 0 129 0 6 2 6 1 6 0 ', '0 0 0 0 0 0 0 0 ');") 

spellTemplate = Template("INSERT INTO `character_spell` VALUES ('$char_guid', '$spell_id', '1', '0');\n")

factionTemplate = Template("INSERT INTO `character_reputation` VALUES ('$char_guid', '$faction_id', '$faction_standing', '1');\n")

singleMacroTemplate = Template("""MACRO $macro_guid "$macro_name" INV_Misc_QuestionMark\\n$macro_body\\nEND\\n""")

macroTemplate = Template("""INSERT INTO `character_account_data` VALUES ('$char_guid', '4', '0', `$macros`);
""")

inventoryList = ""
instanceList = ""
petList = ""
actionList = ""
factionList = ""
macroList = ""

slotMap = {"head" : 0, "neck" : 1, "shoulder" : 2, "chest" : 4, "waist" : 5, "legs" : 6, "feet" : 7, "wrist" : 8, "hands" : 9, "finger1" : 10, "finger2" : 11, "trinket1" : 12, "trinket2" : 13, "back" : 14, "main_hand" : 15, "off_hand" : 16, "relic" : 17, "tabard" : 18}

races = {"Human" : 1, "Orc" : 2, "Dwarf" : 3, "Night Elf" : 4, "Undead" : 5,  "Tauren" : 6, "Gnome" : 7, "Troll" : 8, "Blood Elf" : 10, "Draenei" : 11}
classes = {"warrior" : 1, "paladin" : 2, "hunter" : 3, "rogue" : 4, "priest" : 5, "shaman" : 7, "mage" : 8, "warlock" : 9, "druid" : 11}

skillmap = {"paladin" : {"armor" : [293], "weapons" : [44, 172, 54, 160, 43, 55, 229, 162, 95]},
            "warrior" : {"armor" : [293], "weapons" : [44, 172, 54, 160, 43, 55, 229, 45, 226, 46, 136, 176, 162, 95, 118]},
            "hunter" : {"armor" : [413], "weapons" : [44, 172, 54, 226, 173, 45, 46, 229, 136, 43, 55, 176, 162, 473, 95, 118]},
            "rogue" : {"armor" : [], "weapons" : [45, 226, 173, 46, 54, 43, 176, 162, 95, 118]},
            "priest" : {"armor" : [], "weapons" : [173, 54, 136, 228, 95]},
            "shaman" : {"armor" : [413], "weapons" : [44, 173, 54, 136, 172, 160, 473, 162, 95, 118]},
            "mage" : {"armor" : [], "weapons" : [173, 136, 43, 162, 228, 95]},
            "warlock" : {"armor" : [], "weapons" : [173, 136, 43, 162, 228, 95]},
            "druid" : {"armor" : [], "weapons" : [173, 54, 136, 160, 162, 473, 95]}}

actionMap = {"spell": 0, "macro": 64, "item": 128}

professionMap = {"enchanting" : [13262, 7412, 7413, 13920, 28029, 7411],
                 "engineering" : [4037, 4038, 12656, 30350, 4036, 20219, 20222],
                 "blacksmithing" : [9788, 3100, 3538, 9785, 29844, 2018, 17041, 17040, 17039, 9787],
                 "jewelcrafting" : [25230, 28894, 28895, 28897, 25229, 31252],
                 "leatherworking" : [10656, 10658, 3104, 3811, 10662, 32549, 2108, 10660],
                 "tailoring" : [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908],
                 "cooking" : [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908],
                 "firstaid" : [3274, 3273, 7924, 10846, 27028]}

professionSkillMap = {"enchanting" : 333, "engineering" : 202, "blacksmithing" : 164, "jewelcrafting" : 755, "leatherworking" : 165, "tailoring" : 197, "cooking" : 185, "firstaid" : 192}

professionSpellMap = {"enchanting" : 28029, "engineering": 30350, "blacksmithing" : 29844, "jewelcrafting": 28897, "leatherworking": 32549, "tailoring": 26790, "cooking": 33359, "firstaid": 27028}

genericPetModelMap = {"Bat" : 7894, "Bear" : 706, "Boar" : 4714, "Carrion Bird": 20348, "Cat" : 9954, "Crab" : 699, "Crocolisk" : 2850, "Dragonhawk" : 20263, "Gorilla" : 8129, "Hyena" : 10904, "Nether Ray" : 20098, "Bird of Prey" : 10831, "Raptor" : 19758, "Ravager" : 20063, "Scorpid" : 15433, "Serpent" : 4312, "Spider" : 17180, "Sporebat" : 17751, "Tallstrider" : 38, "Turtle" : 5027, "Warp Stalker" : 19998, "Wind Serpent" : 3204, "Wolf" : 741}

filePath = ""

suffixTable = {"0": [0,0,0], "5": [2802,2803,0], "6": [2804,2803,0], "7": [2803,2805,0], "8": [2806,2803,0], "9": [2804,2806,0], "10": [2804,2805,0], "11": [2802,2804,0], "12": [2806,2805,0], "13": [2802,2806,0], "14": [2802,2805,0], "15": [2806,0,0], "16": [2803,0,0], "17": [2805,0,0], "18": [2802,0,0], "19": [2804,0,0], "20": [2825,0,0], "21": [2807,0,0], "22": [2808,0,0], "23": [2810,0,0], "24": [2809,0,0], "25": [2811,0,0,0], "26": [2812,0,0], "27": [2813,0,0], "28": [2814,0,0], "29": [2815,2802,0], "30": [2816,0,0], "31": [2803,2817,0], "32": [2803,2818,0], "33": [2803,2819,0], "34": [2803,2820,0], "35": [2803,2821,0], "36": [2803,2804,2824], "37": [2803,2804,2812], "38": [2804,2806,2812], "39": [2804,2824,2822], "40": [2802,2803,2825], "41": [2805,2802,2803], "42": [2803,2806,2812], "43": [2805,2803,2823], "44": [2803,2804,2816], "45": [2805,2803,2813], "47": [2826,2805,0], "48": [2805,2906,2824], "49": [2805,2802,2803], "50": [2825,2802,2804], "51": [2824,2822,2804], "52": [2824,2804,2813], "53": [2824,2804,2803], "54": [2805,2823,2803], "55": [2811,2803,2804], "56": [2805,2803,2823], "57": [2825,2802,2803], "58": [2824,2803,2804], "59": [2804,2803,2806], "60": [2825,2803,2802], "61": [2812,0,0], "62": [2805,0,0], "63": [2802,0,0], "64": [2825,0,0], "65": [2824,0,0], "66": [2803,2813,2824]}

if len(sys.argv) == 1:
    print("Usage: ./importer.py path_to_qe_file")
if len(sys.argv) > 1:
    filePath = sys.argv[1]

if os.path.isfile(filePath): 
    with open(filePath) as file:
        file_contents = file.readlines()
        char_class = file_contents[3].split("=")[0]
        char_name = file_contents[3].split("=")[1].replace('"', '').replace('\n', '')
        char_race = file_contents[5].split("=")[1].replace('\n', '')
        char_gender = file_contents[6].split("=")[1].replace('\n', '')
        itemguiditr = 10000
        char_guid = 500
        skills = ""
        spells=""
        equipOffset = 14

        armor_skill = skillmap[char_class]["armor"]
        weapon_skills = skillmap[char_class]["weapons"]

        char_class = classes[char_class]
        char_race = races[char_race]

        if len(armor_skill) > 0:
            skills += skillsTemplate.safe_substitute(char_guid = char_guid, skill_id = armor_skill[0], current_skill=1, max_skill=1)
        for weaponSkill in weapon_skills:
            skills+=skillsTemplate.safe_substitute(char_guid = char_guid, skill_id = weaponSkill, current_skill=350, max_skill=350)

        slots = ["head", "neck", "shoulder", "chest", "waist", "legs", "feet", "wrist", "hands", "finger1", "finger2", "trinket1", "trinket2", "back", "main_hand", "off_hand", "relic", "tabard"]
        for slot in slots:
            for i in range(19):
                if slot in (file_contents[i+equipOffset]):
                    itemInfo = file_contents[i+equipOffset].split(',')
                    suffix = str(0)
                    if len(itemInfo) == 4:
                        suffix = itemInfo[2].split("=")[1]
                    enchant_1 = suffixTable[suffix][0]
                    enchant_2 = suffixTable[suffix][1]
                    enchant_3 = suffixTable[suffix][2]
                    item_entry = file_contents[i+equipOffset].split("=")[2].split(',')[0].replace('\n', '')
                    inventoryList += wornTemplate.safe_substitute(char_guid = char_guid, slot_id = slotMap[slot], item_guid = itemguiditr, item_entry = item_entry, bag_id=0)
                    instanceList += instanceTemplate.safe_substitute(char_guid = char_guid, item_guid = itemguiditr, item_entry = item_entry, item_count=1, item_suffix=-int(suffix), enchant_1=enchant_1, enchant_2=enchant_2, enchant_3=enchant_3)
                    itemguiditr += 2

        # PET
        petFamily = 0
        petHealth = 30000
        petPower = 100
        modelId = 18923
        for i in range(equipOffset, 40):
            if "pet" in file_contents[i]:
                petInfo = file_contents[i].split(',')
                petName = petInfo[0].split('=')[1].replace('\n', '')
                petEntry = petInfo[2].split('=')[1].replace('\n', '')
                if len(petInfo) == 6:
                    petFamily = petInfo[3].split("=")[1].replace('\n', '')
                    modelId = genericPetModelMap[petFamily]
                    petHealth = petInfo[4].split("=")[1].replace('\n', '')
                    petPower = petInfo[5].split("=")[1].replace('\n', '')
                petList = petTemplate.safe_substitute(pet_entry=petEntry, pet_owner=char_guid, pet_name=petName, pet_model=modelId, pet_health=petHealth, pet_resource=petPower)
                break

        # Bag Items
        gearStart=0
        for line in file_contents:
            if "GEAR FROM BAG" in line:
                gearStart = gearStart+1
                break
            else:
                gearStart = gearStart+1
        talentsStart=0
        for line in file_contents:
            if "TALENTS" in line:
                talentsStart = talentsStart+1
                break
            else:
                talentsStart = talentsStart+1
        actionsStart=0
        for line in file_contents:
            if "ACTIONS" in line:
                actionsStart = actionsStart+1
                break
            else:
                actionsStart = actionsStart+1
        macrosStart=0
        for line in file_contents:
            if "MACROS" in line:
                macrosStart = macrosStart+1
                break
            else:
                macrosStart = macrosStart+1
        spellsStart=0
        for line in file_contents:
            if "SPELLS" in line:
                spellsStart = spellsStart+1
                break
            else:
                spellsStart = spellsStart+1
        factionStart=0
        for line in file_contents:
            if "FACTIONS" in line:
                factionStart = factionStart+1
                break
            else:
                factionStart = factionStart+1
        file_eol = len(file_contents)
        
        bagGearArray = []
        talentsArray = []
        actionsArray = []
        macrosArray = []
        spellsArray = []
        factionArray = []

        for i in range(gearStart,talentsStart-2):
            bagGearArray.append(file_contents[i])
        for i in range(talentsStart,actionsStart-2):
            talentsArray.append(file_contents[i])
        for i in range(actionsStart,macrosStart-2):
            actionsArray.append(file_contents[i])
        for i in range(macrosStart,spellsStart-2):
            macrosArray.append(file_contents[i])
        for i in range(spellsStart,factionStart-2):
            spellsArray.append(file_contents[i])
        for i in range(factionStart, file_eol-2):
            factionArray.append(file_contents[i].replace('\n', ''))

        firstSlot = 23+14
        bagID = 1
        for item in bagGearArray:
            suffix = str(0)
            item_data = item.split(",")
            item_count = ""
            item_entry = item_data[0].split("=")
            if len(item_entry) > 1:
                item_entry = item_entry[1]
            if len(item_data) > 1:
                item_count = item_data[1].split("=")[1].replace('\n', '')
            if len(item_data) == 4:
                item_count = item_data[3].split("=")[1].replace('\n', '')
                suffix = item_data[1].split("=")[1]
            enchant_1 = suffixTable[suffix][0]
            enchant_2 = suffixTable[suffix][1]
            enchant_3 = suffixTable[suffix][2]
            slotID = firstSlot%28
            bagID = int(firstSlot/28) + 216
            inventoryList += wornTemplate.safe_substitute(char_guid = char_guid, slot_id = slotID, item_guid = itemguiditr, item_entry = item_entry, bag_id=bagID)
            instanceList += instanceTemplate.safe_substitute(char_guid = char_guid, item_guid = itemguiditr, item_entry = item_entry, item_count=item_count, item_suffix=-int(suffix), enchant_1=enchant_1, enchant_2=enchant_2, enchant_3=enchant_3)
            itemguiditr += 2
            firstSlot += 1

        learnedProfessions = {"enchanting" : False, "engineering" : False, "blacksmithing" : False, "jewelcrafting" : False, "leatherworking" : False, "tailoring" : False, "cooking" : False, "firstaid" : False}

        for spell in spellsArray:
            spell = int(spell)
            if spell == 348700:
                spell = 31892
            if spell == 348704:
                spell = 31801
            spells += spellTemplate.safe_substitute(char_guid=char_guid, spell_id=spell)

            for profession in professionMap:
                if learnedProfessions[profession]:
                    continue;
                if int(spell) in professionMap[profession]:
                    learnedProfessions[profession] = True
                    skills+=skillsTemplate.safe_substitute(char_guid = char_guid, skill_id = professionSkillMap[profession], current_skill=375, max_skill=375)
                    if str(professionSpellMap[profession])+'\n' not in spellsArray:
                        spells += spellTemplate.safe_substitute(char_guid=char_guid, spell_id=professionSpellMap[profession])
        
        spells += spellTemplate.safe_substitute(char_guid=char_guid, spell_id=34093)

        for action in actionsArray:
            actionInfo = action.split(",")
            slot = actionInfo[0].split("=")[1]
            actiontype = actionInfo[1].split("=")[1]
            actionId = actionInfo[2].split("=")[1].replace('\n', '')
            slot = int(slot) - 1
            actionList += actionTemplate.safe_substitute(char_guid=char_guid, slot_id=slot, action_id=actionId, action_type=actionMap[actiontype])

        for faction in factionArray:
            factionInfo = faction.split(",")
            factionId = factionInfo[0]
            factionStanding = factionInfo[1]
            factionList += factionTemplate.safe_substitute(char_guid=char_guid, faction_id=factionId, faction_standing=factionStanding)
        
        if False: # Deactivated because of lacking serverside support
            macroArrayArray = []
            miniMacroArray = []
            macroCounter = 0
            macroMeta = {}
            for macro in macrosArray:
                if len(macro.split(",")) > 1:
                    macroInfo = macro.split(",")
                    if "slot" in macroInfo[0]:
                        macroSlot = macroInfo[0].split("=")[1]
                        macroName = macroInfo[1].split("=")[1]
                        macroTexture = macroInfo[2].split("=")[1]
                        macroMeta[macroSlot] = [macroName, macroTexture]
            for macro in macrosArray:
                if ("---" in macro) and (macroCounter == 0):
                    macroCounter += 1
                    continue
                if ("---" in macro) and (macroCounter > 0):
                    macroArrayArray.append(miniMacroArray)
                    miniMacroArray = []
                    macroCounter = 0
                    continue
                if macroCounter > 0:
                    miniMacroArray.append(macro.replace('\n', ''))
                    macroCounter += 1
                    continue
            i = 0
            for metaMacro in macroMeta:
                macroMeta[metaMacro].append(macroArrayArray[i])
                i += 1
            
            macroBodies = ""

            for macroSlot in macroMeta:
                fullMacro = macroMeta[macroSlot]
                macroBody = ""
                for bodyPart in fullMacro[2]:
                    macroBody += bodyPart + "\\n"
                macroBody = macroBody.rstrip('\n')
                actualBody = singleMacroTemplate.safe_substitute(macro_guid=16777217+int(macroSlot), macro_body=macroBody, macro_name=fullMacro[0])
                macroBodies+=actualBody
            macroList += macroTemplate.safe_substitute(macros="", char_guid=char_guid)

        instanceList = instanceList.rstrip('\n')
        inventoryList = inventoryList.rstrip('\n')
        spells = spells.rstrip('\n')
        actionList = actionList.rstrip('\n')
        factionList = factionList.rstrip('\n')
        skills = skills.rstrip('\n')

        pDumpContent = pdumpTemplate.safe_substitute(char_guid = char_guid, char_name=char_name, char_race=char_race, char_class=char_class, char_gender=char_gender, skills=skills, actions=actionList, inventory_list = inventoryList, pets=petList, spells=spells, instance_list = instanceList, factions=factionList, macros='')
        
        pDumpContent = pDumpContent.rstrip('\n')

        with open("char_dump.sql", "w") as writer:
            writer.write(pDumpContent)
            print("Character conversion successful!")
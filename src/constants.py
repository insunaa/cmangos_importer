from string import Template as Template_base
import sys
import os.path


class Template(Template_base):
    # monkeypatch to avoid rstrip and char_guid everywhere

    def fill(self, **kwds: object) -> str:
        if "no_char_guid" not in kwds:
            kwds["char_guid"] = char_guid

        for k, v in kwds.items():
            if isinstance(v,str):
                kwds[k] = v.rstrip("\n")

        return super().safe_substitute(**kwds) #.rstrip("\n")


# region constants
pet_list = ""
action_list = ""
faction_list = ""
macro_list = ""
skills = ""
spells = ""
inventory_list = ""
instance_list = ""
itemguiditr = 10000
char_guid = 500
equip_offset = 14
learned_professions = {
    "enchanting": False,
    "engineering": False,
    "blacksmithing": False,
    "jewelcrafting": False,
    "leatherworking": False,
    "tailoring": False,
    "cooking": False,
    "firstaid": False,
}
# endregion

# region mappings
slotMap = {
    "head": 0,
    "neck": 1,
    "shoulder": 2,
    "chest": 4,
    "waist": 5,
    "legs": 6,
    "feet": 7,
    "wrist": 8,
    "hands": 9,
    "finger1": 10,
    "finger2": 11,
    "trinket1": 12,
    "trinket2": 13,
    "back": 14,
    "main_hand": 15,
    "off_hand": 16,
    "relic": 17,
    "tabard": 18,
}

races = {
    "Human": 1,
    "Orc": 2,
    "Dwarf": 3,
    "Night Elf": 4,
    "Undead": 5,
    "Tauren": 6,
    "Gnome": 7,
    "Troll": 8,
    "Blood Elf": 10,
    "Draenei": 11,
}

classes = {
    "warrior": 1,
    "paladin": 2,
    "hunter": 3,
    "rogue": 4,
    "priest": 5,
    "shaman": 7,
    "mage": 8,
    "warlock": 9,
    "druid": 11,
}

skillmap = {
    "paladin": {"armor": [293], "weapons": [44, 172, 54, 160, 43, 55, 229, 162, 95]},
    "warrior": {
        "armor": [293],
        "weapons": [44, 172, 54, 160, 43, 55, 229, 45, 226, 46, 136, 176, 162, 95, 118],
    },
    "hunter": {
        "armor": [413],
        "weapons": [
            44,
            172,
            54,
            226,
            173,
            45,
            46,
            229,
            136,
            43,
            55,
            176,
            162,
            473,
            95,
            118,
        ],
    },
    "rogue": {"armor": [], "weapons": [45, 226, 173, 46, 54, 43, 176, 162, 95, 118]},
    "priest": {"armor": [], "weapons": [173, 54, 136, 228, 95]},
    "shaman": {
        "armor": [413],
        "weapons": [44, 173, 54, 136, 172, 160, 473, 162, 95, 118],
    },
    "mage": {"armor": [], "weapons": [173, 136, 43, 162, 228, 95]},
    "warlock": {"armor": [], "weapons": [173, 136, 43, 162, 228, 95]},
    "druid": {"armor": [], "weapons": [173, 54, 136, 160, 162, 473, 95]},
}

actionMap = {"spell": 0, "macro": 64, "item": 128}

professionMap = {
    "enchanting": [13262, 7412, 7413, 13920, 28029, 7411],
    "engineering": [4037, 4038, 12656, 30350, 4036, 20219, 20222],
    "blacksmithing": [9788, 3100, 3538, 9785, 29844, 2018, 17041, 17040, 17039, 9787],
    "jewelcrafting": [25230, 28894, 28895, 28897, 25229, 31252],
    "leatherworking": [10656, 10658, 3104, 3811, 10662, 32549, 2108, 10660],
    "tailoring": [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908],
    "cooking": [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908],
    "firstaid": [3274, 3273, 7924, 10846, 27028],
}
all_prof_skill_ids = [v1 for v in professionMap.values() for v1 in v]


professionSkillMap = {
    "enchanting": 333,
    "engineering": 202,
    "blacksmithing": 164,
    "jewelcrafting": 755,
    "leatherworking": 165,
    "tailoring": 197,
    "cooking": 185,
    "firstaid": 192,
}

professionSpellMap = {
    "enchanting": 28029,
    "engineering": 30350,
    "blacksmithing": 29844,
    "jewelcrafting": 28897,
    "leatherworking": 32549,
    "tailoring": 26790,
    "cooking": 33359,
    "firstaid": 27028,
}

genericPetModelMap = {
    "Bat": 7894,
    "Bear": 706,
    "Boar": 4714,
    "Carrion Bird": 20348,
    "Cat": 9954,
    "Crab": 699,
    "Crocolisk": 2850,
    "Dragonhawk": 20263,
    "Gorilla": 8129,
    "Hyena": 10904,
    "Nether Ray": 20098,
    "Bird of Prey": 10831,
    "Raptor": 19758,
    "Ravager": 20063,
    "Scorpid": 15433,
    "Serpent": 4312,
    "Spider": 17180,
    "Sporebat": 17751,
    "Tallstrider": 38,
    "Turtle": 5027,
    "Warp Stalker": 19998,
    "Wind Serpent": 3204,
    "Wolf": 741,
}

suffixTable = {
    "0": [0, 0, 0],
    "5": [2802, 2803, 0],
    "6": [2804, 2803, 0],
    "7": [2803, 2805, 0],
    "8": [2806, 2803, 0],
    "9": [2804, 2806, 0],
    "10": [2804, 2805, 0],
    "11": [2802, 2804, 0],
    "12": [2806, 2805, 0],
    "13": [2802, 2806, 0],
    "14": [2802, 2805, 0],
    "15": [2806, 0, 0],
    "16": [2803, 0, 0],
    "17": [2805, 0, 0],
    "18": [2802, 0, 0],
    "19": [2804, 0, 0],
    "20": [2825, 0, 0],
    "21": [2807, 0, 0],
    "22": [2808, 0, 0],
    "23": [2810, 0, 0],
    "24": [2809, 0, 0],
    "25": [2811, 0, 0, 0],
    "26": [2812, 0, 0],
    "27": [2813, 0, 0],
    "28": [2814, 0, 0],
    "29": [2815, 2802, 0],
    "30": [2816, 0, 0],
    "31": [2803, 2817, 0],
    "32": [2803, 2818, 0],
    "33": [2803, 2819, 0],
    "34": [2803, 2820, 0],
    "35": [2803, 2821, 0],
    "36": [2803, 2804, 2824],
    "37": [2803, 2804, 2812],
    "38": [2804, 2806, 2812],
    "39": [2804, 2824, 2822],
    "40": [2802, 2803, 2825],
    "41": [2805, 2802, 2803],
    "42": [2803, 2806, 2812],
    "43": [2805, 2803, 2823],
    "44": [2803, 2804, 2816],
    "45": [2805, 2803, 2813],
    "47": [2826, 2805, 0],
    "48": [2805, 2906, 2824],
    "49": [2805, 2802, 2803],
    "50": [2825, 2802, 2804],
    "51": [2824, 2822, 2804],
    "52": [2824, 2804, 2813],
    "53": [2824, 2804, 2803],
    "54": [2805, 2823, 2803],
    "55": [2811, 2803, 2804],
    "56": [2805, 2803, 2823],
    "57": [2825, 2802, 2803],
    "58": [2824, 2803, 2804],
    "59": [2804, 2803, 2806],
    "60": [2825, 2803, 2802],
    "61": [2812, 0, 0],
    "62": [2805, 0, 0],
    "63": [2802, 0, 0],
    "64": [2825, 0, 0],
    "65": [2824, 0, 0],
    "66": [2803, 2813, 2824],
}
# endregion

# region sql
pdumpTemplate = Template(
    """IMPORTANT NOTE: This sql queries not created for apply directly, use '.pdump load' command in console or client chat instead.
IMPORTANT NOTE: NOT APPLY ITS DIRECTLY to character DB or you will DAMAGE and CORRUPT character DB

UPDATE character_db_version SET required_s2429_01_characters_raf = 1 WHERE FALSE;

INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '70', '0', '300000000', '0', '0', '65568', '-1817.69', '5321.56', '-12.4282', '530', '0', '1.86449', '2 0 0 8 0 0 1048576 0 0 0 0 0 0 0 0 0 ', '0', '1', '200', '175', '1642414101', '1', '0', '0', '0', '0', '0', '0', '0', '0', '10', '0', '0', '3703', '0', '', '0', '0', '0', '0', '0', '0', '0', '0', '2147483647', '0', '5594', '0', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', NULL, '0', '0 0 ', '0', '0', NULL, NULL, NULL);
INSERT INTO `character_homebind` VALUES ('$char_guid', '530', '3703', '-1817.69', '5321.56', '-12.4282');
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '24', '184', '6948'); -- Hearthstone
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '19', '217', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '22', '218', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '21', '219', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '20', '220', '23162'); -- Large Bag
$inventory_list$pet_list
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
"""
)

skillsTemplate = Template(
    """INSERT INTO `character_skills` VALUES ('$char_guid', '$skill_id', '$current_skill', '$max_skill');
"""
)

wornTemplate = Template(
    """INSERT INTO `character_inventory` VALUES ('$char_guid', '$bag_id', '$slot_id', '$item_guid', '$item_entry');
"""
)

instanceTemplate = Template(
    """INSERT INTO `item_instance` VALUES ('$item_guid', '$char_guid', '$item_entry', '0', '0', '$item_count', '0', '-1 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 0 0 0 ', '$item_suffix', '100', '0');
"""
)

actionTemplate = Template(
    "INSERT INTO `character_action` VALUES ('$char_guid', '$slot_id', '$action_id', '$action_type');\n"
)

petTemplate = Template(
    "\nINSERT INTO `character_pet` VALUES ('10000', '$pet_entry', '$pet_owner', '$pet_model', '13481', '1', '70', '0', '1', '1000', '6', '0', '300', '$pet_name', '1', '0', '$pet_health', '$pet_resource', '157750', '1642440972', '0', '0', '7 2 7 1 7 0 129 0 129 0 129 0 129 0 6 2 6 1 6 0 ', '0 0 0 0 0 0 0 0 ');"
)

spellTemplate = Template(
    "INSERT INTO `character_spell` VALUES ('$char_guid', '$spell_id', '1', '0');\n"
)

factionTemplate = Template(
    "INSERT INTO `character_reputation` VALUES ('$char_guid', '$faction_id', '$faction_standing', '1');\n"
)

singleMacroTemplate = Template(
    """MACRO $macro_guid "$macro_name" INV_Misc_QuestionMark
$macro_body
END\n"""
)

# endregion

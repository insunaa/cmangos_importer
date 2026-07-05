from __future__ import annotations

import datetime
import time
import warnings
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
from src.constants import (
    Template,
    achievementTemplate,
    actionMap,
    actionTemplate,
    actionTemplateWotLK,
    charactersTemplateTBC,
    charactersTemplateVan,
    charactersTemplateWOTLK,
    classes,
    duplicateSkills,
    equipmentTemplate,
    factions,
    factionTemplate,
    gemIDPropertyMap,
    gemIDPropertyMapWotlk,
    gemPropertyMap,
    gemPropertyMapWotLK,
    genericPetModelMap,
    glyphMap,
    glyphTemplate,
    instanceEnchantTemplateTBC,
    instanceEnchantTemplateVan,
    instanceEnchantTemplateWOTLK,
    instanceTemplate,
    instanceTemplateWotLK,
    itemSocketBonusMap,
    itemSocketBonusMapWotlk,
    pdumpTemplate,
    petTemplate,
    petTemplateWotLK,
    questTemplate,
    questTemplateWotLK,
    races,
    ridingSpellMap,
    singleMacroTemplate,
    skillmap,
    skillsTemplate,
    slotMap,
    slots,
    spellTemplate,
    startPosMap,
    suffixTable,
    suffixTable2,
    talentTemplate,
    tbcSkillMap,
    vanillaSkillMap,
    wornTemplate,
)

# ---------------------------------------------------------------------------
GEM_SLOTS = 3
CHAR_GUID = 500
ITEM_GUID_START = 10000
ITEM_GUID_INCREMENT = 2
EQUIPMENT_SLOT_COUNT = 23
BAG_EQUIP_SLOT_OFFSET = 18
MAIN_ENCHANTS_ZERO_FILL = (0, 0, 0, 0)

SPELL_GENERIC_MOUNT = 34093
SPELL_REMAP_348700 = 31892
SPELL_REMAP_348704 = 31801
RIDER_SKILL_NORMAL = 75
RIDER_SKILL_MAX = 150
SPELL_RIDE60 = 33388
SPELL_RIDE100 = 33391

MACRO_MIN_SLOT = 100
MACRO_GUID_BASE = 16777216
MACRO_GUID_OFFSET = 120
ACHIEVEMENT_YEAR_OFFSET = 2000

DEFAULT_PET_MODEL = 706
DEFAULT_BAG_ID_WOTLK_TBC = 23162
DEFAULT_BAG_ID_VANILLA = 14156

BUCKLE_ENCHANT_ID = 3729

REQUIRED_PLAYER_FIELDS = (
    "name",
    "gender",
    "class",
    "race",
    "level",
    "gold",
    "expansion",
    "locale",
)

_EQUIP_CACHE_SLOTS = (
    ("head", "head"),
    ("neck", "neck"),
    ("shoulder", "shoulder"),
    ("shirt", "shirt"),
    ("chest", "chest"),
    ("waist", "belt"),
    ("legs", "legs"),
    ("feet", "feet"),
    ("wrist", "wrist"),
    ("hands", "gloves"),
    ("back", "back"),
    ("main_hand", "mainhand"),
    ("off_hand", "offhand"),
    ("relic", "ranged"),
    ("tabard", "tabard"),
)


# ---------------------------------------------------------------------------
class ExpansionConfig:
    def __init__(
        self,
        *,
        instance_enchant_template: Template,
        instance_template: Template,
        characters_template: Template,
        pet_template: Template,
        action_template: Template,
        quest_template: Template,
        gem_property_map: dict,
        gem_id_property_map: dict,
        socket_bonus_map: dict,
        version_sql: str,
        default_bag_id: int,
        negate_suffix: bool,
        is_wotlk: bool = False,
    ) -> None:
        self.instance_enchant_template = instance_enchant_template
        self.instance_template = instance_template
        self.characters_template = characters_template
        self.pet_template = pet_template
        self.action_template = action_template
        self.quest_template = quest_template
        self.gem_property_map = gem_property_map
        self.gem_id_property_map = gem_id_property_map
        self.socket_bonus_map = socket_bonus_map
        self.version_sql = version_sql
        self.default_bag_id = default_bag_id
        self.negate_suffix = negate_suffix
        self.is_wotlk = is_wotlk


_EXPAN_CONFIGS: Dict[int, ExpansionConfig] = {
    0: ExpansionConfig(
        instance_enchant_template=instanceEnchantTemplateVan,
        instance_template=instanceTemplate,
        characters_template=charactersTemplateVan,
        pet_template=petTemplate,
        action_template=actionTemplate,
        quest_template=questTemplate,
        gem_property_map={},
        gem_id_property_map={},
        socket_bonus_map={},
        version_sql="required_z2819_01_characters_item_instance_text_id_fix",
        default_bag_id=DEFAULT_BAG_ID_VANILLA,
        negate_suffix=False,
    ),
    1: ExpansionConfig(
        instance_enchant_template=instanceEnchantTemplateTBC,
        instance_template=instanceTemplate,
        characters_template=charactersTemplateTBC,
        pet_template=petTemplate,
        action_template=actionTemplate,
        quest_template=questTemplate,
        gem_property_map=gemPropertyMap,
        gem_id_property_map=gemIDPropertyMap,
        socket_bonus_map=itemSocketBonusMap,
        version_sql="required_s2473_01_characters_item_instance_text_id_fix",
        default_bag_id=DEFAULT_BAG_ID_WOTLK_TBC,
        negate_suffix=True,
    ),
    2: ExpansionConfig(
        instance_enchant_template=instanceEnchantTemplateWOTLK,
        instance_template=instanceTemplateWotLK,
        characters_template=charactersTemplateWOTLK,
        pet_template=petTemplateWotLK,
        action_template=actionTemplateWotLK,
        quest_template=questTemplateWotLK,
        gem_property_map=gemPropertyMapWotLK,
        gem_id_property_map=gemIDPropertyMapWotlk,
        socket_bonus_map=itemSocketBonusMapWotlk,
        version_sql="required_14061_01_characters_fishingSteps",
        default_bag_id=DEFAULT_BAG_ID_WOTLK_TBC,
        negate_suffix=True,
        is_wotlk=True,
    ),
}


def _exp_config(exp: int) -> ExpansionConfig:
    return _EXPAN_CONFIGS[exp]


# ---------------------------------------------------------------------------
@dataclass
class ParseOutput:
    inventory_list: str = ""
    instance_list: str = ""
    item_guid: int = ITEM_GUID_START
    spells: str = ""
    skills: str = ""
    talents: str = ""
    action_list: str = ""
    faction_list: str = ""
    quests: str = ""
    glyphs: str = ""
    achievements: str = ""
    char_skills: str = ""
    pet_list: str = ""
    class_name: str = ""


# ---------------------------------------------------------------------------
def _default_gems() -> List[Dict[str, object]]:
    return [{"id": 0, "matched": False} for _ in range(GEM_SLOTS)]


def _pad_gems(raw_gems: Optional[List[Dict]]) -> List[Dict[str, object]]:
    result = _default_gems()
    for i, gem in enumerate(raw_gems or []):
        if i < GEM_SLOTS:
            result[i] = {"id": int(gem["id"]), "matched": bool(gem["matched"])}
    return result


def _normalize_item_fields(item: Dict) -> Dict[str, str]:
    suffix_raw = item.get("suffix", 0)
    enchant_raw = item.get("enchantId", 0)
    buckle_raw = item.get("buckle")
    return {
        "suffix": str(suffix_raw) if suffix_raw else "0",
        "enchant": str(enchant_raw) if enchant_raw else "0",
        "gems": _pad_gems(item.get("gems")),
        "buckle": str(buckle_raw).lower() if buckle_raw is not None else "false",
    }


def _lookup_suffix_enchants(suffix_str: str) -> Tuple[int, int, int]:
    if suffix_str in suffixTable:
        vals = suffixTable[suffix_str]
        return (vals[0], vals[1], vals[2])
    if suffix_str in suffixTable2:
        vals = suffixTable2[suffix_str]
        return (vals[0], vals[1], vals[2])
    return MAIN_ENCHANTS_ZERO_FILL


def _build_enchantments_vanilla(
    enchant: str,
    suffix_str: str,
) -> str:
    e1, e2, e3 = _lookup_suffix_enchants(suffix_str)
    return instanceEnchantTemplateVan.fill(
        main_enchant=enchant,
        enchant_1=e1,
        enchant_2=e2,
        enchant_3=e3,
    )


def _resolve_socket_bonus(
    matched: List[bool],
    item_entry: int,
    socket_bonus_map: dict,
) -> int:
    if False not in matched and True in matched and item_entry in socket_bonus_map:
        return socket_bonus_map[item_entry]
    return 0


def _resolve_gem_values(
    gem_ids: List[int],
    gem_id_property_map: dict,
    gem_property_map: dict,
) -> Tuple[int, int, int]:
    return (
        gem_property_map[gem_id_property_map[int(gem_ids[0])]],
        gem_property_map[gem_id_property_map[int(gem_ids[1])]],
        gem_property_map[gem_id_property_map[int(gem_ids[2])]],
    )


def _build_enchantments_post_vanilla(
    enchant: str,
    suffix_str: str,
    matched: List[bool],
    item_entry: int,
    buckle: str,
    config: ExpansionConfig,
    gem_ids: List[int],
) -> str:
    socket_bonus = _resolve_socket_bonus(matched, item_entry, config.socket_bonus_map)

    if config.is_wotlk and suffix_str not in suffixTable:
        suffix_str = "0"

    g1, g2, g3 = _resolve_gem_values(
        gem_ids,
        config.gem_id_property_map,
        config.gem_property_map,
    )

    e1, e2, e3 = _lookup_suffix_enchants(suffix_str)

    if config.is_wotlk and buckle != "false":
        e1 = BUCKLE_ENCHANT_ID

    return config.instance_enchant_template.fill(
        main_enchant=enchant,
        gem1=g1,
        gem2=g2,
        gem3=g3,
        socket_bonus=socket_bonus,
        enchant_1=e1,
        enchant_2=e2,
        enchant_3=e3,
    )


def _build_enchantments(
    exp: int,
    enchant: str,
    suffix_str: str,
    matched: List[bool],
    item_entry: int,
    buckle: str,
    config: ExpansionConfig,
    gem_ids: List[int],
) -> str:
    if exp == 0:
        return _build_enchantments_vanilla(enchant, suffix_str)

    return _build_enchantments_post_vanilla(
        enchant,
        suffix_str,
        matched,
        item_entry,
        buckle,
        config,
        gem_ids,
    )


def _add_to_itemlists(
    output: ParseOutput,
    exp: int,
    slot_id: int,
    item_entry: str,
    suffix: str,
    enchant: str,
    gems: List[Dict[str, object]],
    buckle: str,
    *,
    bag_id: str = "0",
    item_count: int = 1,
) -> None:
    suffix = abs(int(suffix))

    output.inventory_list += wornTemplate.fill(
        slot_id=slot_id,
        item_guid=output.item_guid,
        item_entry=item_entry,
        bag_id=bag_id,
    )

    config = _exp_config(exp)
    matched = [gems[0]["matched"], gems[1]["matched"], gems[2]["matched"]]
    gem_ids = [gems[0]["id"], gems[1]["id"], gems[2]["id"]]

    enchantments = _build_enchantments(
        exp, enchant, str(suffix), matched, int(item_entry), buckle, config, gem_ids
    )

    effective_suffix = -suffix if config.negate_suffix else suffix

    output.instance_list += config.instance_template.fill(
        item_guid=output.item_guid,
        item_entry=item_entry,
        item_count=item_count,
        item_suffix=effective_suffix,
        enchantments=enchantments,
    )

    output.item_guid += ITEM_GUID_INCREMENT


# ---------------------------------------------------------------------------
def _parse_equipment(
    data: Dict,
    output: ParseOutput,
    exp: int,
    slot_cache: Dict[str, int],
) -> None:
    equipment = data.get("equipment", {})
    for slot_name, item in equipment.items():
        if slot_name not in slotMap:
            warnings.warn(f"Unknown equipment slot '{slot_name}', skipping item.")
            continue

        fields = _normalize_item_fields(item)

        _add_to_itemlists(
            output,
            exp,
            slotMap[slot_name],
            item["id"],
            fields["suffix"],
            fields["enchant"],
            fields["gems"],
            fields["buckle"],
        )
        slot_cache[slot_name] = item["id"]


# ---------------------------------------------------------------------------
def _parse_pet(
    data: Dict,
    char_class_id: int,
    output: ParseOutput,
    exp: int,
) -> None:
    if char_class_id != classes["hunter"]:
        return

    pet_data = data.get("pet")
    if not pet_data:
        return

    config = _exp_config(exp)

    family_name = pet_data.get("family")
    model_id = (
        genericPetModelMap.get(family_name, DEFAULT_PET_MODEL)
        if family_name
        else DEFAULT_PET_MODEL
    )

    pet_list = config.pet_template.fill(
        no_char_guid=True,
        pet_entry=str(pet_data["id"]),
        pet_owner=CHAR_GUID,
        pet_name=pet_data["name"],
        pet_level=str(pet_data["level"]),
        pet_model=model_id,
        pet_health=int(pet_data.get("health", 30000)),
        pet_resource=int(pet_data.get("power", 100)),
    )

    output.pet_list = pet_list


# ---------------------------------------------------------------------------
def _parse_bag_contents(
    data: Dict,
    output: ParseOutput,
    exp: int,
) -> None:
    bag_entries = data.get("bagContents", [])
    if not bag_entries:
        return

    # First pass: assign deterministic GUIDs to container entries
    container_guid_map = {}
    container_idx = 0
    for item in bag_entries:
        if "count" not in item and "slot" not in item:
            bag_num = int(item["bag"])
            container_guid_map[bag_num] = ITEM_GUID_START + (
                container_idx * ITEM_GUID_INCREMENT
            )
            container_idx += 1

    # Second pass: actually add everything
    for i, item in enumerate(bag_entries):
        if "count" not in item and "slot" not in item:
            slot_id = int(item["bag"]) + BAG_EQUIP_SLOT_OFFSET
            fields = {"suffix": "0", "enchant": "0"}
            fields.update(
                gems=_default_gems(),
                buckle="false",
            )
            _add_to_itemlists(
                output,
                exp,
                slot_id,
                item["id"],
                fields["suffix"],
                fields["enchant"],
                fields["gems"],
                fields["buckle"],
            )
            continue

        bag_num = int(item["bag"])
        if bag_num in container_guid_map:
            inv_bag_id = str(container_guid_map[bag_num])
            slot_id = int(item["slot"]) - 1
        else:
            inv_bag_id = "0"
            slot_id = int(item["slot"]) - 1 + EQUIPMENT_SLOT_COUNT
        fields = _normalize_item_fields(item)

        _add_to_itemlists(
            output,
            exp,
            slot_id,
            item["id"],
            fields["suffix"],
            fields["enchant"],
            fields["gems"],
            fields["buckle"],
            bag_id=inv_bag_id,
            item_count=item.get("count", 1),
        )


# ---------------------------------------------------------------------------
def _parse_spells(
    data: Dict,
    char_level: str,
    output: ParseOutput,
    exp: int,
) -> None:
    raw_spells = data.get("spells", [])
    seen: set = set()

    if exp > 0 and SPELL_GENERIC_MOUNT not in raw_spells:
        output.spells += spellTemplate.fill(spell_id=SPELL_GENERIC_MOUNT)
        seen.add(SPELL_GENERIC_MOUNT)

    for spell in raw_spells:
        spell_id = int(spell)

        if spell_id == 348700:
            spell_id = SPELL_REMAP_348700
        elif spell_id == 348704:
            spell_id = SPELL_REMAP_348704

        if spell_id in seen:
            continue

        if exp == 0 and spell_id in ridingSpellMap:
            riding_skill = RIDER_SKILL_NORMAL
            riding_spell = SPELL_RIDE60
            if char_level == "60":
                riding_skill = RIDER_SKILL_MAX
                riding_spell = SPELL_RIDE100

            output.skills += skillsTemplate.fill(
                skill_id=ridingSpellMap[spell_id],
                current_skill=riding_skill,
                max_skill=riding_skill,
            )
            if riding_spell not in seen:
                output.spells += spellTemplate.fill(spell_id=riding_spell)
                seen.add(riding_spell)

        seen.add(spell_id)
        output.spells += spellTemplate.fill(spell_id=spell_id)


# ---------------------------------------------------------------------------
def _parse_talents(
    data: Dict,
    output: ParseOutput,
    exp: int,
) -> None:
    if exp < 2:
        return

    raw_talents = data.get("talents", [])
    for talent in raw_talents:
        rank = talent["rank"]
        if rank == 0:
            continue
        output.talents += talentTemplate.fill(
            talent_id=talent["id"],
            current_rank=rank,
        )


# ---------------------------------------------------------------------------
def _parse_actions(
    data: Dict,
    output: ParseOutput,
    exp: int,
) -> None:
    config = _exp_config(exp)
    raw_actions = data.get("actions", [])
    for action in raw_actions:
        action_type_name = action["type"]
        if action_type_name not in actionMap:
            warnings.warn(
                f"Unknown action type '{action_type_name}' "
                f"(action id={action.get('id')}), skipping."
            )
            continue

        output.action_list += config.action_template.fill(
            slot_id=int(action["slot"]) - 1,
            action_id=str(action["id"]),
            action_type=actionMap[action_type_name],
        )


# ---------------------------------------------------------------------------
def _parse_factions(
    data: Dict,
    output: ParseOutput,
) -> None:
    raw_factions = data.get("factions", [])
    for faction in raw_factions:
        output.faction_list += factionTemplate.fill(
            faction_id=faction["factionID"],
            faction_standing=faction["earnedValue"],
        )


# ---------------------------------------------------------------------------
def _parse_macros(data: Dict) -> str:
    macro_bodies = ""
    raw_macros = data.get("macros", [])
    for macro in raw_macros:
        slot_num = int(macro["slot"])
        if slot_num < MACRO_MIN_SLOT:
            warnings.warn(
                f"Macro '{macro.get('name', '?')}' in slot {slot_num} "
                f"is below minimum ({MACRO_MIN_SLOT}), skipping."
            )
            continue

        body_lines = macro["body"].replace("@", "target=")
        actual_body = singleMacroTemplate.fill(
            macro_guid=MACRO_GUID_BASE + slot_num - MACRO_GUID_OFFSET,
            macro_body=body_lines,
            macro_name=macro["name"],
        )
        macro_bodies += actual_body

    _write_macros(macro_bodies)
    return macro_bodies


def _write_macros(macro_file: str) -> None:
    with open("macros-cache.txt", "w") as writer:
        writer.write(macro_file)


# ---------------------------------------------------------------------------
def _parse_quests(
    data: Dict,
    output: ParseOutput,
    exp: int,
) -> None:
    config = _exp_config(exp)
    raw_quests = data.get("quests", [])
    for quest_id in raw_quests:
        output.quests += config.quest_template.fill(quest_id=quest_id)


# ---------------------------------------------------------------------------
def _parse_glyphs(
    data: Dict,
    output: ParseOutput,
) -> None:
    raw_glyphs = data.get("glyphs", [])
    for glyph in raw_glyphs:
        glyph_spell = glyph["spellID"]
        if glyph_spell not in glyphMap:
            warnings.warn(
                f"Glyph spell {glyph_spell} not found in glyph map, skipping."
            )
            continue
        output.glyphs += glyphTemplate.fill(
            glyph_slot=glyph["socket"] - 1,
            glyph_id=glyphMap[glyph_spell],
        )


# ---------------------------------------------------------------------------
def _add_default_skills(char_class: str, char_level: int, output: ParseOutput) -> None:
    armor_skill = skillmap[char_class]["armor"]
    weapon_skills = skillmap[char_class]["weapons"]
    level_int = int(char_level)

    if armor_skill:
        output.skills += skillsTemplate.fill(
            skill_id=armor_skill[0],
            current_skill=1,
            max_skill=1,
        )
    for ws in weapon_skills:
        output.skills += skillsTemplate.fill(
            skill_id=ws,
            current_skill=level_int * 5,
            max_skill=level_int * 5,
        )


def _parse_achievements(
    data: Dict,
    output: ParseOutput,
) -> None:
    raw_achievements = data.get("achievements", [])
    for ach in raw_achievements:
        date_time = datetime.datetime(
            ach["year"] + ACHIEVEMENT_YEAR_OFFSET, ach["month"], ach["day"], 0, 0
        )
        timestamp = time.mktime(date_time.timetuple())
        output.achievements += achievementTemplate.fill(
            achievement_id=ach["id"],
            timestamp=timestamp,
        )


# ---------------------------------------------------------------------------
def _parse_char_skills(
    data: Dict,
    char_locale: str,
    output: ParseOutput,
    exp: int,
) -> None:
    if char_locale not in vanillaSkillMap and char_locale not in tbcSkillMap:
        print("Your client's language is not currently supported for skill export")
        return

    raw_skills = data.get("skills", [])
    class_name = output.class_name

    if exp == 0:
        skill_map = vanillaSkillMap.get(char_locale, {})
        map_label = "Vanilla"
    elif exp == 1:
        skill_map = tbcSkillMap.get(char_locale, {})
        map_label = "TBC"
    else:
        print("WotLK not supported for skill export yet")
        return

    dup_skills = duplicateSkills.get(char_locale, {})

    for skill in raw_skills:
        skill_name = skill["name"]
        skill_rank = int(skill["rank"])
        max_rank = int(skill["maxRank"])

        skill_id = 0
        if skill_name in dup_skills:
            skill_id = dup_skills[skill_name].get(class_name, 0)
        elif skill_name in skill_map:
            skill_id = skill_map[skill_name]
        else:
            print(f"Skill not found in {map_label} skill map")

        output.char_skills += skillsTemplate.fill(
            skill_id=skill_id,
            current_skill=skill_rank,
            max_skill=max_rank,
        )


# ---------------------------------------------------------------------------
def _empty_enchant(exp: int) -> str:
    if exp == 0:
        return instanceEnchantTemplateVan.fill(
            main_enchant=0, enchant_1=0, enchant_2=0, enchant_3=0
        )
    elif exp == 1:
        return instanceEnchantTemplateTBC.fill(
            main_enchant=0,
            gem1=0,
            gem2=0,
            gem3=0,
            socket_bonus=0,
            enchant_1=0,
            enchant_2=0,
            enchant_3=0,
        )
    else:
        return instanceEnchantTemplateWOTLK.fill(
            main_enchant=0,
            gem1=0,
            gem2=0,
            gem3=0,
            socket_bonus=0,
            enchant_1=0,
            enchant_2=0,
            enchant_3=0,
        )


def _fill_equipment_cache(slot_cache: Dict[str, int]) -> str:
    cache_values = {v: slot_cache[k] for k, v in _EQUIP_CACHE_SLOTS}
    return equipmentTemplate.fill(**cache_values)


def _write_pdump(
    char_info: Dict[str, str],
    slot_cache: Dict[str, int],
    output: ParseOutput,
    exp: int,
) -> None:
    config = _exp_config(exp)

    start_pos = startPosMap[exp][factions[char_info["char_race_key"]]]
    pos_x, pos_y, pos_z, start_map = start_pos

    equipment_cache = _fill_equipment_cache(slot_cache)

    if exp == 2:
        empty_enchant = instanceEnchantTemplateWOTLK.fill(
            main_enchant=0,
            gem1=0,
            gem2=0,
            gem3=0,
            socket_bonus=0,
            enchant_1=0,
            enchant_2=0,
            enchant_3=0,
            equipmentCache=equipment_cache,
        )
        characters_row = config.characters_template.fill(
            **char_info,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z,
            start_map=start_map,
        )
    else:
        empty_enchant = _empty_enchant(exp)
        characters_row = config.characters_template.fill(
            **char_info,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z,
            start_map=start_map,
            equipmentCache=equipment_cache,
        )

    result = pdumpTemplate.fill(
        bag_id=config.default_bag_id,
        characters_row=characters_row,
        enchantments=empty_enchant,
        database_version=config.version_sql,
        pos_x=pos_x,
        pos_y=pos_y,
        pos_z=pos_z,
        start_map=start_map,
        skills=output.char_skills,
        actions=output.action_list,
        quests=output.quests,
        inventory_list=output.inventory_list,
        pet_list=output.pet_list,
        spells=output.spells,
        talents=output.talents,
        instance_list=output.instance_list,
        factions=output.faction_list,
        text=", ''" if exp == 2 else "",
        glyphs=output.glyphs,
        achievements=output.achievements,
    )

    rand_no = datetime.datetime.now().strftime("%H%M%S")
    filename = char_info["char_name"] + rand_no + ".sql"
    with open(filename, "w") as writer:
        writer.write(result)
        print("Character conversion successful! Export written to: " + filename)


# ---------------------------------------------------------------------------
def parse_file(data: Dict, exp: int) -> None:
    output = ParseOutput()

    player = data.get("player")
    if not player:
        raise ValueError("Input JSON is missing the required 'player' section.")

    missing = [f for f in REQUIRED_PLAYER_FIELDS if f not in player]
    if missing:
        raise ValueError(
            f"Player data is missing required fields: {', '.join(missing)}"
        )

    char_class_raw = player["class"]
    if char_class_raw not in classes:
        raise ValueError(f"Unknown character class '{char_class_raw}'.")
    if char_class_raw not in skillmap:
        raise ValueError(
            f"No skill mapping for class '{char_class_raw}'. "
            "The class may need to be added to constants.skillmap."
        )

    char_race_raw = player["race"]
    if char_race_raw not in races:
        raise ValueError(f"Unknown character race '{char_race_raw}'.")
    if char_race_raw not in factions:
        raise ValueError(
            f"No faction mapping for race '{char_race_raw}'. "
            "The race may need to be added to constants.factions."
        )

    slot_cache: Dict[str, int] = {slot: 0 for slot in slots}

    output.class_name = char_class_raw
    char_info: Dict[str, str] = dict(
        char_name=player["name"],
        char_gender=str(player["gender"]),
        char_class=classes[char_class_raw],
        char_race=races[char_race_raw],
        char_level=str(player["level"]),
        char_money=str(player["gold"]),
        char_expansion=str(player["expansion"]),
        char_locale=player["locale"],
        char_health="10000",
        char_power="0",
    )
    char_info["char_race_key"] = char_race_raw

    _add_default_skills(char_class_raw, char_info["char_level"], output)

    _parse_bag_contents(data, output, exp)
    _parse_equipment(data, output, exp, slot_cache)
    _parse_pet(data, classes[char_class_raw], output, exp)
    _parse_spells(data, char_info["char_level"], output, exp)
    _parse_talents(data, output, exp)
    _parse_actions(data, output, exp)
    _parse_factions(data, output)
    _parse_macros(data)
    _parse_quests(data, output, exp)
    _parse_glyphs(data, output)
    _parse_achievements(data, output)
    _parse_char_skills(data, char_info["char_locale"], output, exp)
    _write_pdump(char_info, slot_cache, output, exp)

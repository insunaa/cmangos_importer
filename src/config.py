from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import (
    actionTemplate,
    actionTemplateWotLK,
    charactersTemplateTBC,
    charactersTemplateVan,
    charactersTemplateWOTLK,
    gemIDPropertyMap,
    gemIDPropertyMapWotlk,
    gemPropertyMap,
    gemPropertyMapWotLK,
    instanceEnchantTemplateTBC,
    instanceEnchantTemplateVan,
    instanceEnchantTemplateWOTLK,
    instanceTemplate,
    instanceTemplateWotLK,
    itemSocketBonusMap,
    itemSocketBonusMapWotlk,
    petTemplate,
    petTemplateWotLK,
    questTemplate,
    questTemplateWotLK,
)
from src.models import ExpansionConfig

# ---------------------------------------------------------------------------
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

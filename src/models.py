from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
class ExpansionConfig:
    def __init__(
        self,
        *,
        instance_enchant_template,
        instance_template,
        characters_template,
        pet_template,
        action_template,
        quest_template,
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


# ---------------------------------------------------------------------------
@dataclass
class ParseOutput:
    inventory_list: str = ""
    instance_list: str = ""
    item_guid: int = 10000
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

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import (
    duplicateSkills,
    skillmap,
    skillsTemplate,
    tbcSkillMap,
    vanillaSkillMap,
)


# ---------------------------------------------------------------------------
def _add_default_skills(char_class: str, char_level: int, output) -> None:
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


# ---------------------------------------------------------------------------
def _parse_char_skills(data: Dict, char_locale: str, output, exp: int) -> None:
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

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.config import (
    RIDER_SKILL_MAX,
    RIDER_SKILL_NORMAL,
    SPELL_GENERIC_MOUNT,
    SPELL_REMAP_348700,
    SPELL_REMAP_348704,
    SPELL_RIDE60,
    SPELL_RIDE100,
)
from src.constants import ridingSpellMap, skillsTemplate, spellTemplate


# ---------------------------------------------------------------------------
def _parse_spells(
    data: Dict,
    char_level: str,
    output,
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

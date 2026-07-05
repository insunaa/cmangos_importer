# BSD 3-Clause License.
#
# Copyright (c) 2025, cmangos_importer contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

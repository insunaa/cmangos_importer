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

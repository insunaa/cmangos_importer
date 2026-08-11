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

"""Thin orchestrator -- validates input JSON and runs the parse pipeline."""

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.config import REQUIRED_PLAYER_FIELDS
from src.constants import classes, factions, races, skillmap, slots
from src.models import ParseOutput
from src.output import _write_pdump
from src.parsers.achievements import _parse_achievements
from src.parsers.actions import _parse_actions
from src.parsers.bags import _parse_bag_contents
from src.parsers.equipment import _parse_equipment
from src.parsers.factions import _parse_factions
from src.parsers.glyphs import _parse_glyphs
from src.parsers.macros import _parse_macros
from src.parsers.pet import _parse_pet
from src.parsers.quests import _parse_quests
from src.parsers.skills import _add_default_skills, _parse_char_skills
from src.parsers.spells import _parse_spells
from src.parsers.talents import _parse_talents


# ---------------------------------------------------------------------------
def parse_file(data: Dict, exp: int) -> None:
    """Parse a GearExporter JSON and write the character pdump SQL file."""
    output = ParseOutput()

    # -- validate player data --------------------------------------------------
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

    # -- build slot cache and char info ----------------------------------------
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

    # -- run parse pipeline ----------------------------------------------------
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

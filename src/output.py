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

import datetime
from typing import Dict

# ---------------------------------------------------------------------------
from src.config import _EQUIP_CACHE_SLOTS, _exp_config
from src.constants import (
    equipmentTemplate,
    instanceEnchantTemplateTBC,
    instanceEnchantTemplateVan,
    instanceEnchantTemplateWOTLK,
    pdumpTemplate,
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


# ---------------------------------------------------------------------------
def _fill_equipment_cache(slot_cache: Dict[str, int]) -> str:
    cache_values = {v: slot_cache[k] for k, v in _EQUIP_CACHE_SLOTS}
    return equipmentTemplate.fill(**cache_values)


# ---------------------------------------------------------------------------
def _write_pdump(
    char_info: Dict[str, str], slot_cache: Dict[str, int], output, exp: int
) -> None:
    config = _exp_config(exp)

    from src.constants import factions, startPosMap

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
        )
        characters_row = config.characters_template.fill(
            **char_info,
            pos_x=pos_x,
            pos_y=pos_y,
            pos_z=pos_z,
            start_map=start_map,
            equipmentCache=equipment_cache,
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

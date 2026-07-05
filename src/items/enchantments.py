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

from typing import List, Tuple

from src.config import BUCKLE_ENCHANT_ID, MAIN_ENCHANTS_ZERO_FILL, _exp_config

# ---------------------------------------------------------------------------
from src.constants import suffixTable, suffixTable2


# ---------------------------------------------------------------------------
def _lookup_suffix_enchants(suffix_str: str) -> Tuple[int, int, int]:
    if suffix_str in suffixTable:
        vals = suffixTable[suffix_str]
        return (vals[0], vals[1], vals[2])
    if suffix_str in suffixTable2:
        vals = suffixTable2[suffix_str]
        return (vals[0], vals[1], vals[2])
    return MAIN_ENCHANTS_ZERO_FILL


# ---------------------------------------------------------------------------
def _resolve_socket_bonus(
    matched: List[bool],
    item_entry: int,
    socket_bonus_map: dict,
) -> int:
    if False not in matched and True in matched and item_entry in socket_bonus_map:
        return socket_bonus_map[item_entry]
    return 0


# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
def _build_enchantments_vanilla(enchant: str, suffix_str: str) -> str:
    from src.constants import instanceEnchantTemplateVan

    e1, e2, e3 = _lookup_suffix_enchants(suffix_str)
    return instanceEnchantTemplateVan.fill(
        main_enchant=enchant,
        enchant_1=e1,
        enchant_2=e2,
        enchant_3=e3,
    )


# ---------------------------------------------------------------------------
def _build_enchantments_post_vanilla(
    enchant: str,
    suffix_str: str,
    matched: List[bool],
    item_entry: int,
    buckle: str,
    config,
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


# ---------------------------------------------------------------------------
def _build_enchantments(
    exp: int,
    enchant: str,
    suffix_str: str,
    matched: List[bool],
    item_entry: int,
    buckle: str,
    gem_ids: List[int],
) -> str:
    if exp == 0:
        return _build_enchantments_vanilla(enchant, suffix_str)

    config = _exp_config(exp)
    return _build_enchantments_post_vanilla(
        enchant,
        suffix_str,
        matched,
        item_entry,
        buckle,
        config,
        gem_ids,
    )

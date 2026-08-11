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

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

"""Re-exports for backward compatibility -- delegates to focused data modules."""

from src.data.action_data import actionMap, talentArray
from src.data.gems import (
    gemIDPropertyMap,
    gemIDPropertyMapWotlk,
    gemPropertyMap,
    gemPropertyMapWotLK,
)
from src.data.glyphs_data import glyphMap
from src.data.identity import (
    classes,
    factions,
    genericPetModelMap,
    races,
    slotMap,
    slots,
    startPosMap,
)
from src.data.skills_data import (
    duplicateSkills,
    ridingSpellMap,
    skillmap,
    tbcSkillMap,
    vanillaSkillMap,
)
from src.data.socket_bonus import itemSocketBonusMap, itemSocketBonusMapWotlk
from src.data.sql_templates import (
    achievementTemplate,
    actionTemplate,
    actionTemplateWotLK,
    charactersTemplateTBC,
    charactersTemplateVan,
    charactersTemplateWOTLK,
    equipmentTemplate,
    factionTemplate,
    glyphTemplate,
    instanceEnchantTemplateTBC,
    instanceEnchantTemplateVan,
    instanceEnchantTemplateWOTLK,
    instanceTemplate,
    instanceTemplateWotLK,
    pdumpTemplate,
    petTemplate,
    petTemplateWotLK,
    questTemplate,
    questTemplateWotLK,
    singleMacroTemplate,
    skillsTemplate,
    spellTemplate,
    talentTemplate,
    wornTemplate,
)
from src.data.suffixes import suffixTable, suffixTable2
from src.data.template import Template, char_guid

__all__ = [
    # template utility
    "Template",
    "char_guid",
    # identity
    "slotMap",
    "slots",
    "startPosMap",
    "factions",
    "races",
    "classes",
    "genericPetModelMap",
    # skills
    "tbcSkillMap",
    "vanillaSkillMap",
    "duplicateSkills",
    "skillmap",
    "ridingSpellMap",
    # gems
    "gemPropertyMap",
    "gemPropertyMapWotLK",
    "gemIDPropertyMap",
    "gemIDPropertyMapWotlk",
    # socket bonuses
    "itemSocketBonusMap",
    "itemSocketBonusMapWotlk",
    # actions & talents
    "actionMap",
    "talentArray",
    # glyphs
    "glyphMap",
    # suffixes
    "suffixTable",
    "suffixTable2",
    # SQL templates
    "pdumpTemplate",
    "equipmentTemplate",
    "instanceEnchantTemplateWOTLK",
    "instanceEnchantTemplateTBC",
    "instanceEnchantTemplateVan",
    "charactersTemplateWOTLK",
    "charactersTemplateTBC",
    "charactersTemplateVan",
    "skillsTemplate",
    "wornTemplate",
    "instanceTemplate",
    "instanceTemplateWotLK",
    "actionTemplate",
    "actionTemplateWotLK",
    "petTemplate",
    "petTemplateWotLK",
    "spellTemplate",
    "talentTemplate",
    "factionTemplate",
    "questTemplate",
    "questTemplateWotLK",
    "glyphTemplate",
    "achievementTemplate",
    "singleMacroTemplate",
]

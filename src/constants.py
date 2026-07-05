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

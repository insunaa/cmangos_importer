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

"""SQL INSERT statement templates for all character tables."""

from src.data.template import Template

pdumpTemplate = Template(
    """IMPORTANT NOTE: This sql queries not created for apply directly, use '.pdump load' command in console or client chat instead.
IMPORTANT NOTE: NOT APPLY ITS DIRECTLY to character DB or you will DAMAGE and CORRUPT character DB

UPDATE character_db_version SET $database_version = 1 WHERE FALSE;

$characters_row
$achievements
$glyphs
INSERT INTO `character_homebind` VALUES ('$char_guid', '$start_map', '3703', '$pos_x', '$pos_y', '$pos_z');
$quests
$inventory_list$pet_list
$skills
$spells
$talents
$instance_list
$actions
$factions
"""
)

equipmentTemplate = Template(
    "$head 0 $neck 0 $shoulder 0 $shirt 0 $chest 0 $belt 0 $legs 0 $feet 0 $wrist 0 $gloves 0 0 0 0 0 0 0 0 0 $back 0 $mainhand 0 $offhand 0 $ranged 0 $tabard 0"
)

instanceEnchantTemplateWOTLK = Template(
    "$main_enchant 0 0 0 0 0 $gem1 0 0 $gem2 0 0 $gem3 0 0 $socket_bonus 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 0 0 0 0 0 0 "
)
instanceEnchantTemplateTBC = Template(
    "$main_enchant 0 0 0 0 0 $gem1 0 0 $gem2 0 0 $gem3 0 0 $socket_bonus 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 0 0 0 "
)
instanceEnchantTemplateVan = Template(
    "$main_enchant 0 0 0 0 0 0 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 "
)

charactersTemplateWOTLK = Template(
    "INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '$char_level', '0', '$char_money', '0', '0', '65568', '$pos_x', '$pos_y', '$pos_z', '$start_map', '0', '4.13832', '2 0 0 8 0 0 1048576 0 0 0 0 0 0 0 ', '0', '1', '200', '175', '1669632358', '1', '0', '0', '0', '0', '0', '0', '0', '0', '8', '0', '8', '4395', '0', '', '5000', '75000', '0', '0', '0', '0', '0', '0', '0', '4294967295', '0', '$char_health', '$char_power', '0', '0', '100', '0', '0', '0', '1', '0', '0 0 0 0 0 0 1048576 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 512 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4194304 256 0 0 0 0 0 0 0 0 67108864 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '$equipmentCache', '0', '0 0 0 0 0 0 ', '0', '0', '0', NULL, NULL, NULL);"
)
charactersTemplateTBC = Template(
    "INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '$char_level', '0', '$char_money', '0', '0', '65568', '$pos_x', '$pos_y', '$pos_z', '$start_map', '0', '1.86449', '2 0 0 8 0 0 1048576 0 0 0 0 0 0 0 0 0 ', '0', '1', '200', '175', '1642414101', '1', '0', '0', '0', '0', '0', '0', '0', '0', '10', '0', '0', '3703', '0', '', '0', '0', '0', '0', '0', '0', '0', '0', '2147483647', '0', '5594', '0', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', '$equipmentCache', '0', '0 0 ', '0', '0', '0', NULL, NULL, NULL);"
)
charactersTemplateVan = Template(
    "INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '$char_level', '0', '$char_money', '0', '0', '0', '$pos_x', '$pos_y', '$pos_z', '$start_map', '2.70526', '1024 0 0 0 0 0 0 0 ', '0', '1', '0', '0', '1642834034', '1', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '32', '0', '0', '', '0', '0', '0', '0', '0', '0', '0', '63', '79', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', '$equipmentCache', '0', '0', '0', '0', NULL, NULL, NULL);"
)

skillsTemplate = Template(
    """INSERT INTO `character_skills` VALUES ('$char_guid', '$skill_id', '$current_skill', '$max_skill');
"""
)

wornTemplate = Template(
    """INSERT INTO `character_inventory` VALUES ('$char_guid', '$bag_id', '$slot_id', '$item_guid', '$item_entry');
"""
)

instanceTemplate = Template(
    """INSERT INTO `item_instance` VALUES ('$item_guid', '$char_guid', '$item_entry', '0', '0', '$item_count', '0', '-1 0 0 0 0 ', '1', '$enchantments', '$item_suffix', '100', '0');
"""
)

instanceTemplateWotLK = Template(
    """INSERT INTO `item_instance` VALUES ('$item_guid', '$char_guid', '$item_entry', '0', '0', '$item_count', '0', '0 0 0 0 0 ', '1', '$enchantments', '$item_suffix', '60', '0', '');
"""
)

actionTemplate = Template(
    "INSERT INTO `character_action` VALUES ('$char_guid', '$slot_id', '$action_id', '$action_type');\n"
)

actionTemplateWotLK = Template(
    "INSERT INTO `character_action` VALUES ('$char_guid', '0', '$slot_id', '$action_id', '$action_type');\n"
)

petTemplate = Template(
    "\nINSERT INTO `character_pet` VALUES ('10000', '$pet_entry', '$pet_owner', '$pet_model', '13481', '1', '$pet_level', '0', '1', '1000', '6', '0', '300', '$pet_name', '1', '0', '$pet_health', '$pet_resource', '157750', '1642440972', '0', '0', '7 2 7 1 7 0 129 0 129 0 129 0 129 0 6 2 6 1 6 0 ', '0 0 0 0 0 0 0 0 ');"
)

petTemplateWotLK = Template(
    "\nINSERT INTO `character_pet` VALUES ('10000', '$pet_entry', '$pet_owner', '$pet_model', '13481', '1', '$pet_level', '0', '1', '$pet_name', '1', '0', '$pet_health', '$pet_resource', '157750', '1642440972', '0', '0', '7 2 7 1 7 0 129 0 129 0 129 0 129 0 6 2 6 1 6 0 ');"
)

spellTemplate = Template(
    "INSERT INTO `character_spell` VALUES ('$char_guid', '$spell_id', '1', '0');\n"
)

talentTemplate = Template(
    "INSERT INTO `character_talent` VALUES ('$char_guid', '$talent_id', '$current_rank', '0');\n"
)

factionTemplate = Template(
    "INSERT INTO `character_reputation` VALUES ('$char_guid', '$faction_id', '$faction_standing', '1');\n"
)

questTemplate = Template(
    "INSERT INTO `character_queststatus` VALUES ('$char_guid', '$quest_id', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');\n"
)

questTemplateWotLK = Template(
    "INSERT INTO `character_queststatus` VALUES ('$char_guid', '$quest_id', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');\n"
)

glyphTemplate = Template(
    "INSERT INTO `character_glyphs` VALUES ('$char_guid', '0', '$glyph_slot', '$glyph_id');\n"
)

achievementTemplate = Template(
    "INSERT INTO `character_achievement` VALUES ('$char_guid', '$achievement_id', '$timestamp');\n"
)

singleMacroTemplate = Template(
    """MACRO $macro_guid "$macro_name" INV_Misc_QuestionMark
$macro_body
END\n"""
)

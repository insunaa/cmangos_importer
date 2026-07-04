import datetime
import time

from src.constants import *


def _pad_gems(raw_gems):
    """Normalize gem data from JSON (list of dicts) to the internal format:
    exactly 3 entries, each a dict with 'id' (int) and 'matched' (bool).
    Missing gems become id=0, matched=False.
    """
    result = [{"id": 0, "matched": False}] * 3
    for i, gem in enumerate(raw_gems):
        if i < 3:
            result[i] = {"id": int(gem["id"]), "matched": bool(gem["matched"])}
    return result


def parse_file(data, exp):
    slotCache = {}
    for slot in slots:
        slotCache[slot] = 0

    player = data["player"]

    # ---------------------------------------------------------------------
    # Character info
    # ---------------------------------------------------------------------
    global skills, class_name
    char_class = player["class"]
    class_name = char_class
    char_race = player["race"]
    armor_skill = skillmap[char_class]["armor"]
    weapon_skills = skillmap[char_class]["weapons"]

    char_info = dict(
        char_name=player["name"],
        char_gender=str(player["gender"]),
        char_class=classes[char_class],
        char_race=races[char_race],
        char_level=str(player["level"]),
        char_money=str(player["gold"]),
        char_expansion=str(player["expansion"]),
        char_locale=player["locale"],
        char_health=10000,
        char_power=0,
    )

    if len(armor_skill):
        skills += skillsTemplate.fill(
            skill_id=armor_skill[0],
            current_skill=1,
            max_skill=1,
        )
    for weaponSkill in weapon_skills:
        skills += skillsTemplate.fill(
            skill_id=weaponSkill,
            current_skill=int(char_info["char_level"]) * 5,
            max_skill=int(char_info["char_level"]) * 5,
        )

    # ---------------------------------------------------------------------
    # add_to_itemlists — adapted for gem dicts
    # ---------------------------------------------------------------------
    def add_to_itemlists(
        slot_id,
        item_entry,
        suffix,
        enchant,
        gems,
        buckle,
        bag_id="0",
        item_count=1,
        bagno=5,
        worn=False,
        bag_offset=0,
    ):
        global inventory_list, instance_list, itemguiditr
        bagMap = {
            "0": 0,
            "1": 10000 + ((bag_offset + 0) * 2),
            "2": 10000 + ((bag_offset + 1) * 2),
            "3": 10000 + ((bag_offset + 2) * 2),
            "4": 10000 + ((bag_offset + 3) * 2),
        }
        slot_id = int(slot_id)
        socketBonus = 0
        if bag_id != "0" and bagno > 3 and not worn:
            inventory_list += wornTemplate.fill(
                slot_id=slot_id,
                item_guid=itemguiditr,
                item_entry=item_entry,
                bag_id=bagMap[bag_id],
            )
        elif bag_id == "0" and bagno <= 3 and worn:
            inventory_list += wornTemplate.fill(
                slot_id=slot_id - 1,
                item_guid=itemguiditr,
                item_entry=item_entry,
                bag_id=bag_id,
            )
        elif bag_id == "0" and bagno > 3 and not worn:
            inventory_list += wornTemplate.fill(
                slot_id=((slot_id - 1) + 23),
                item_guid=itemguiditr,
                item_entry=item_entry,
                bag_id=bag_id,
            )
        else:
            inventory_list += wornTemplate.fill(
                slot_id=slot_id,
                item_guid=itemguiditr,
                item_entry=item_entry,
                bag_id=bag_id,
            )

        matched = [gems[0]["matched"], gems[1]["matched"], gems[2]["matched"]]
        gem_ids = [gems[0]["id"], gems[1]["id"], gems[2]["id"]]
        suffix = abs(int(suffix))

        enchantments = ""
        if exp == 0:
            if str(suffix) in suffixTable2:
                enchantments = instanceEnchantTemplateVan.fill(
                    main_enchant=enchant,
                    enchant_1=suffixTable2[str(suffix)][0],
                    enchant_2=suffixTable2[str(suffix)][1],
                    enchant_3=suffixTable2[str(suffix)][2],
                )
            elif str(suffix) in suffixTable:
                enchantments = instanceEnchantTemplateVan.fill(
                    main_enchant=enchant,
                    enchant_1=suffixTable[str(suffix)][0],
                    enchant_2=suffixTable[str(suffix)][1],
                    enchant_3=suffixTable[str(suffix)][2],
                )
            else:
                enchantments = instanceEnchantTemplateVan.fill(
                    main_enchant=enchant, enchant_1=0, enchant_2=0, enchant_3=0
                )
        elif exp == 1:
            if False not in matched and True in matched:
                socketBonus = itemSocketBonusMap[int(item_entry)]
            if str(suffix) in suffixTable:
                enchantments = instanceEnchantTemplateTBC.fill(
                    main_enchant=enchant,
                    gem1=gemPropertyMap[gemIDPropertyMap[int(gem_ids[0])]],
                    gem2=gemPropertyMap[gemIDPropertyMap[int(gem_ids[1])]],
                    gem3=gemPropertyMap[gemIDPropertyMap[int(gem_ids[2])]],
                    socket_bonus=socketBonus,
                    enchant_1=suffixTable[str(suffix)][0],
                    enchant_2=suffixTable[str(suffix)][1],
                    enchant_3=suffixTable[str(suffix)][2],
                )
            else:
                enchantments = instanceEnchantTemplateTBC.fill(
                    main_enchant=enchant,
                    gem1=gemPropertyMap[gemIDPropertyMap[int(gem_ids[0])]],
                    gem2=gemPropertyMap[gemIDPropertyMap[int(gem_ids[1])]],
                    gem3=gemPropertyMap[gemIDPropertyMap[int(gem_ids[2])]],
                    socket_bonus=socketBonus,
                    enchant_1=suffixTable[str(suffix)][0],
                    enchant_2=suffixTable[str(suffix)][1],
                    enchant_3=suffixTable[str(suffix)][2],
                )
        elif exp == 2:
            if (
                False not in matched
                and True in matched
                and int(item_entry) in itemSocketBonusMapWotlk
            ):
                socketBonus = itemSocketBonusMapWotlk[int(item_entry)]
            if str(suffix) not in suffixTable:
                suffix = 0
            if buckle == "false":
                enchantments = instanceEnchantTemplateWOTLK.fill(
                    main_enchant=enchant,
                    gem1=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gem_ids[0])]],
                    gem2=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gem_ids[1])]],
                    gem3=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gem_ids[2])]],
                    socket_bonus=socketBonus,
                    enchant_1=suffixTable[str(suffix)][0],
                    enchant_2=suffixTable[str(suffix)][1],
                    enchant_3=suffixTable[str(suffix)][2],
                )
            else:
                enchantments = instanceEnchantTemplateWOTLK.fill(
                    main_enchant=enchant,
                    gem1=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gem_ids[0])]],
                    gem2=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gem_ids[1])]],
                    gem3=gemPropertyMapWotLK[gemIDPropertyMapWotlk[int(gem_ids[2])]],
                    socket_bonus=socketBonus,
                    enchant_1=3729,
                    enchant_2=suffixTable[str(suffix)][1],
                    enchant_3=suffixTable[str(suffix)][2],
                )

        if exp == 0:
            instance_list += instanceTemplate.fill(
                item_guid=itemguiditr,
                item_entry=item_entry,
                item_count=item_count,
                item_suffix=suffix,
                enchantments=enchantments,
            )
        elif exp == 1:
            instance_list += instanceTemplate.fill(
                item_guid=itemguiditr,
                item_entry=item_entry,
                item_count=item_count,
                item_suffix=(-suffix),
                enchantments=enchantments,
            )
        elif exp == 2:
            instance_list += instanceTemplateWotLK.fill(
                item_guid=itemguiditr,
                item_entry=item_entry,
                item_count=item_count,
                item_suffix=-suffix,
                enchantments=enchantments,
            )
        itemguiditr += 2

    # ---------------------------------------------------------------------
    # Equipment
    # ---------------------------------------------------------------------
    def parse_equipment():
        equipment = data.get("equipment", {})
        for slot_name, item in equipment.items():
            if slot_name not in slotMap:
                continue
            suffix = str(item.get("suffix", 0)) or "0"
            enchant = str(item.get("enchantId", 0)) or "0"
            raw_gems = item.get("gems")
            gems = (
                _pad_gems(raw_gems) if raw_gems else [{"id": 0, "matched": False}] * 3
            )
            buckle = (
                str(item.get("buckle", False)).lower()
                if item.get("buckle") is not None
                else "false"
            )

            add_to_itemlists(
                slotMap[slot_name],
                item["id"],
                suffix,
                enchant,
                gems,
                buckle,
                worn=True,
            )
            slotCache[slot_name] = item["id"]

    # ---------------------------------------------------------------------
    # Hunter pet
    # ---------------------------------------------------------------------
    def parse_pet():
        if char_info["char_class"] != classes["hunter"]:
            return
        global pet_list
        pet_data = data.get("pet")
        if not pet_data:
            return
        modelId = 706
        petHealth = int(pet_data.get("health", 30000))
        petPower = int(pet_data.get("power", 100))
        family_name = pet_data.get("family")
        if family_name and family_name in genericPetModelMap:
            modelId = genericPetModelMap[family_name]

        petEntry = str(pet_data["id"])
        petName = pet_data["name"]
        petLevel = str(pet_data["level"])

        if exp < 2:
            pet_list = petTemplate.fill(
                no_char_guid=True,
                pet_entry=petEntry,
                pet_owner=char_guid,
                pet_name=petName,
                pet_level=petLevel,
                pet_model=modelId,
                pet_health=petHealth,
                pet_resource=petPower,
            )
        else:
            pet_list = petTemplateWotLK.fill(
                no_char_guid=True,
                pet_entry=petEntry,
                pet_owner=char_guid,
                pet_name=petName,
                pet_level=petLevel,
                pet_model=modelId,
                pet_health=petHealth,
                pet_resource=petPower,
            )

    # ---------------------------------------------------------------------
    # Bag contents
    # ---------------------------------------------------------------------
    def parse_bag_contents():
        bag_entries = data.get("bagContents", [])
        if not bag_entries:
            return

        # bag_offset must match the number of filled equipment slots (not bags).
        # Equipment is parsed first, so slotCache already reflects what's equipped.
        bag_offset = sum(1 for v in slotCache.values() if v != 0)

        default_gems = [{"id": 0, "matched": False}] * 3

        for item in bag_entries:
            # Summary entries (equipped bags) — only bag + id
            if "count" not in item and "slot" not in item:
                slot_id = int(item["bag"]) + 18
                add_to_itemlists(
                    slot_id,
                    item["id"],
                    suffix=0,
                    enchant=0,
                    bag_id=0,
                    gems=default_gems,
                    buckle="false",
                    bagno=0,
                )
                continue

            bag_id = str(item["bag"])
            slot_id = str(int(item["slot"]) - 1)
            item_count = item.get("count", 1)
            suffix = str(item.get("suffix", 0)) or "0"
            enchant = str(item.get("enchantId", 0)) or "0"
            raw_gems = item.get("gems")
            gems = _pad_gems(raw_gems) if raw_gems else default_gems
            buckle_val = item.get("buckle")
            buckle = str(buckle_val).lower() if buckle_val is not None else "false"

            add_to_itemlists(
                slot_id,
                item["id"],
                suffix,
                enchant,
                gems,
                buckle,
                bag_id=bag_id,
                item_count=item_count,
                bag_offset=bag_offset,
            )

    # ---------------------------------------------------------------------
    # Spells
    # ---------------------------------------------------------------------
    def parse_spells():
        global spells, skills
        spellList = []
        raw_spells = data.get("spells", [])
        if exp > 0 and 34093 not in raw_spells:
            spells += spellTemplate.fill(spell_id=34093)
            spellList.append(34093)
        for spell in raw_spells:
            spell = int(spell)
            if spell == 348700:
                spell = 31892
            if spell == 348704:
                spell = 31801
            if spell in spellList:
                continue
            if exp == 0 and spell in ridingSpellMap:
                riding_skill = 75
                riding_spell = 33388
                if char_info["char_level"] == "60":
                    riding_skill = 150
                    riding_spell = 33391
                skills += skillsTemplate.fill(
                    skill_id=ridingSpellMap[spell],
                    current_skill=riding_skill,
                    max_skill=riding_skill,
                )
                if riding_spell not in spellList:
                    spells += spellTemplate.fill(spell_id=riding_spell)
                    spellList.append(riding_spell)
            spellList.append(spell)
            spells += spellTemplate.fill(spell_id=spell)

    # ---------------------------------------------------------------------
    # Talents (from JSON, only for WotLK+)
    # ---------------------------------------------------------------------
    def parse_talents():
        global talents
        raw_talents = data.get("talents", [])
        if exp < 2:
            return
        for talent in raw_talents:
            rank = talent["rank"]
            if rank == 0:
                continue
            talents += talentTemplate.fill(
                talent_id=talent["id"],
                current_rank=rank,
            )

    # ---------------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------------
    def parse_actions():
        global action_list
        raw_actions = data.get("actions", [])
        for action in raw_actions:
            slot = int(action["slot"]) - 1
            actiontype = action["type"]
            actionId = str(action["id"])
            if actiontype not in actionMap:
                continue
            if exp != 2:
                action_list += actionTemplate.fill(
                    slot_id=slot,
                    action_id=actionId,
                    action_type=actionMap[actiontype],
                )
            else:
                action_list += actionTemplateWotLK.fill(
                    slot_id=slot,
                    action_id=actionId,
                    action_type=actionMap[actiontype],
                )

    # ---------------------------------------------------------------------
    # Factions
    # ---------------------------------------------------------------------
    def parse_factions():
        global faction_list
        raw_factions = data.get("factions", [])
        for faction in raw_factions:
            faction_list += factionTemplate.fill(
                faction_id=faction["factionID"],
                faction_standing=faction["earnedValue"],
            )

    # ---------------------------------------------------------------------
    # Macros
    # ---------------------------------------------------------------------
    def parse_macros():
        macroBodies = ""
        raw_macros = data.get("macros", [])
        for macro in raw_macros:
            slot_num = int(macro["slot"])
            if slot_num < 100:
                continue
            body_lines = macro["body"].replace("@", "target=")
            actual_body = singleMacroTemplate.fill(
                macro_guid=16777216 + slot_num - 120,
                macro_body=body_lines,
                macro_name=macro["name"],
            )
            macroBodies += actual_body
        write_macros(macroBodies)

    # ---------------------------------------------------------------------
    # Quests
    # ---------------------------------------------------------------------
    def parse_quests():
        global quests
        raw_quests = data.get("quests", [])
        for quest_id in raw_quests:
            if exp > 1:
                quests += questTemplateWotLK.fill(quest_id=quest_id)
            else:
                quests += questTemplate.fill(quest_id=quest_id)

    # ---------------------------------------------------------------------
    # Glyphs (Cataclysm only)
    # ---------------------------------------------------------------------
    def parse_glyphs():
        global glyphs
        raw_glyphs = data.get("glyphs", [])
        for glyph in raw_glyphs:
            glyphspell = glyph["spellID"]
            if glyphspell in glyphMap:
                glyphs += glyphTemplate.fill(
                    glyph_slot=glyph["socket"] - 1,
                    glyph_id=glyphMap[glyphspell],
                )

    # ---------------------------------------------------------------------
    # Achievements (Cataclysm only)
    # ---------------------------------------------------------------------
    def parse_achievements():
        global achievements
        raw_achievements = data.get("achievements", [])
        for ach in raw_achievements:
            date_time = datetime.datetime(
                ach["year"] + 2000, ach["month"], ach["day"], 0, 0
            )
            timestamp = time.mktime(date_time.timetuple())
            achievements += achievementTemplate.fill(
                achievement_id=ach["id"],
                timestamp=timestamp,
            )

    # ---------------------------------------------------------------------
    # Skills
    # ---------------------------------------------------------------------
    def parse_skills():
        global cskills
        locale = char_info["char_locale"]
        if locale not in vanillaSkillMap and locale not in tbcSkillMap:
            print("Your client's language is not currently supported for skill export")
            return
        raw_skills = data.get("skills", [])
        for skill in raw_skills:
            skillName = skill["name"]
            skillRank = int(skill["rank"])
            maxRank = int(skill["maxRank"])
            skill_id = 0
            if exp == 0:
                if skillName in duplicateSkills:
                    skill_id = duplicateSkills[locale][skillName][class_name]
                elif skillName in vanillaSkillMap[locale]:
                    skill_id = vanillaSkillMap[locale][skillName]
                else:
                    print("Skill not found in Vanilla skill map")
            elif exp == 1:
                if skillName in duplicateSkills:
                    skill_id = duplicateSkills[locale][skillName][class_name]
                elif skillName in tbcSkillMap[locale]:
                    skill_id = tbcSkillMap[locale][skillName]
                else:
                    print("Skill not found in TBC skill map")
            else:
                print("WotLK not supported for skill export yet")

            cskills += skillsTemplate.fill(
                skill_id=skill_id,
                current_skill=skillRank,
                max_skill=maxRank,
            )

    # ---------------------------------------------------------------------
    # Write SQL output
    # ---------------------------------------------------------------------
    def write_pdump(char_info):
        start_pos = startPosMap[exp][factions[player["race"]]]
        version = ""
        characters_row = ""
        enchantments = ""
        equipment_cache = equipmentTemplate.fill(
            head=slotCache["head"],
            neck=slotCache["neck"],
            shoulder=slotCache["shoulder"],
            shirt=slotCache["shirt"],
            chest=slotCache["chest"],
            belt=slotCache["waist"],
            legs=slotCache["legs"],
            feet=slotCache["feet"],
            wrist=slotCache["wrist"],
            gloves=slotCache["hands"],
            back=slotCache["back"],
            mainhand=slotCache["main_hand"],
            offhand=slotCache["off_hand"],
            ranged=slotCache["relic"],
            tabard=slotCache["tabard"],
        )
        bagId = 23162
        if exp == 0:
            version = "required_z2819_01_characters_item_instance_text_id_fix"
            enchantments = instanceEnchantTemplateVan.fill(
                main_enchant=0, enchant_1=0, enchant_2=0, enchant_3=0
            )
            bagId = 14156
            characters_row = charactersTemplateVan.fill(
                **char_info,
                pos_x=start_pos[0],
                pos_y=start_pos[1],
                pos_z=start_pos[2],
                start_map=start_pos[3],
                equipmentCache=equipment_cache,
            )
        elif exp == 1:
            version = "required_s2473_01_characters_item_instance_text_id_fix"
            enchantments = instanceEnchantTemplateTBC.fill(
                main_enchant=0,
                gem1=0,
                gem2=0,
                gem3=0,
                socket_bonus=0,
                enchant_1=0,
                enchant_2=0,
                enchant_3=0,
            )
            characters_row = charactersTemplateTBC.fill(
                **char_info,
                pos_x=start_pos[0],
                pos_y=start_pos[1],
                pos_z=start_pos[2],
                start_map=start_pos[3],
                equipmentCache=equipment_cache,
            )
        else:
            version = "required_14061_01_characters_fishingSteps"
            enchantments = instanceEnchantTemplateWOTLK.fill(
                main_enchant=0,
                gem1=0,
                gem2=0,
                gem3=0,
                socket_bonus=0,
                enchant_1=0,
                enchant_2=0,
                enchant_3=0,
                equipmentCache=equipment_cache,
            )
            characters_row = charactersTemplateWOTLK.fill(
                **char_info,
                pos_x=start_pos[0],
                pos_y=start_pos[1],
                pos_z=start_pos[2],
                start_map=start_pos[3],
            )

        result = pdumpTemplate.fill(
            bag_id=bagId,
            characters_row=characters_row,
            enchantments=enchantments,
            database_version=version,
            pos_x=start_pos[0],
            pos_y=start_pos[1],
            pos_z=start_pos[2],
            start_map=start_pos[3],
            skills=cskills,
            actions=action_list,
            quests=quests,
            inventory_list=inventory_list,
            pet_list=pet_list,
            spells=spells,
            talents=talents,
            instance_list=instance_list,
            factions=faction_list,
            text=", ''" if exp == 2 else "",
            glyphs=glyphs,
            achievements=achievements,
        )

        rand_no = datetime.datetime.now().strftime("%H%M%S")
        filename = char_info["char_name"] + rand_no + ".sql"
        with open(filename, "w") as writer:
            writer.write(result)
            print("Character conversion successful! Export written to: " + filename)

    def write_macros(macro_file):
        with open("macros-cache.txt", "w") as writer:
            writer.write(macro_file)

    # ---------------------------------------------------------------------
    # Main execution order
    # ---------------------------------------------------------------------
    parse_equipment()
    parse_pet()
    parse_bag_contents()
    parse_spells()
    parse_talents()
    parse_actions()
    parse_factions()
    parse_macros()
    parse_quests()
    parse_glyphs()
    parse_achievements()
    parse_skills()
    write_pdump(char_info)

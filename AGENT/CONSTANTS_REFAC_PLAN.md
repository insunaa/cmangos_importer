# constants.py Refactoring Plan

**Context**: `src/constants.py` is ~14,238 lines of data tables, SQL templates, and dead code. This document maps every symbol, traces its usage, identifies dead weight, and proposes a logical split.

---

## Symbol Inventory

Every top-level symbol, its line range, size, what it is, and who uses it.

### A. Dead Code (remove immediately)

| Symbol | Lines | Size | Reason |
|---|---|---|---|
| `import os.path` / `import sys` | 1-2 | — | Never referenced anywhere in the project |
| `pet_list`, `action_list`, `faction_list`, `macro_list`, `skills`, `cskills`, `spells`, `talents`, `quests`, `glyphs`, `achievements`, `inventory_list`, `instance_list`, `class_name` | 21-34 | 14 vars | Mutable globals initialized to `""`. Written-to during parsing but never read back. Legacy from when the whole parser lived in one file. Now replaced by `ParseOutput` dataclass. |
| `itemguiditr = 10000` | 35 | — | Shadowed by `ITEM_GUID_START` in `config.py`. Never imported anywhere. |
| `char_guid = 500` | 36 | — | Used only inside `Template.fill()` (below). Not imported elsewhere. Keep, but mark as internal to Template. |
| `equip_offset = 15` | 37 | — | Never used. Shadowed by `BAG_EQUIP_SLOT_OFFSET = 18` in `config.py`. |
| `learned_professions` dict | 38-52 | 15 lines | Never imported or referenced outside this file. Dead code. |
| `maxSkillMap` | 99 | 1 line | Never imported anywhere. |
| `talentArray` | 9551-11530 | **~2,000 lines** | Never imported by any module. The actual talent parsing uses `talentTemplate` (a simple SQL template). This appears to be a legacy WoW talent tree definition table that was never wired in. |

**Dead code total**: ~2,065 lines removable immediately with zero behavioral impact.

### B. Template Utility

| Symbol | Lines | What it is |
|---|---|---|
| `Template` class | 6-17 | Custom `string.Template` subclass that auto-injects `char_guid` into every fill call. Core infrastructure — everything depends on this. |

### C. Character Identity Mappings (small, static)

These map human-readable names to database IDs for character creation. They are small (<50 entries each), stable, and imported by the orchestrator.

| Symbol | Lines | Size | Used by |
|---|---|---|---|
| `slotMap` | 56-75 | 20 lines | `src/parsers/equipment.py` |
| `slots` list | 77-97 | 21 lines | `src/parser.py` (slot_cache init) |
| `startPosMap` | 644-658 | 15 lines | `src/output.py` |
| `factions` | 659-671 | 13 lines | `src/parser.py`, `src/output.py`, `src/config.py` (indirectly) |
| `races` | 672-684 | 13 lines | `src/parser.py` |
| `classes` | 685-697 | 13 lines | `src/parser.py`, `src/parsers/pet.py`, `src/config.py` (indirectly) |

### D. Skill & Profession Mappings

Maps localized skill names to database skill IDs. Locale-specific, expansion-specific.

| Symbol | Lines | Size | Used by |
|---|---|---|---|
| `tbcSkillMap` | 101-375 | ~275 lines | `src/parsers/skills.py` |
| `vanillaSkillMap` | 376-630 | ~255 lines | `src/parsers/skills.py` |
| `duplicateSkills` | 631-643 | ~13 lines | `src/parsers/skills.py` |
| `skillmap` | 698-739 | ~42 lines | `src/parsers/skills.py`, `src/parser.py` |
| `ridingSpellMap` | 740 | 1 line | `src/parsers/spells.py` |
| `professionMap` | 11895-11921 | ~27 lines | Never imported. Dead code. |
| `all_prof_skill_ids` | 11922 | 1 line | Derived from dead `professionMap`. Dead. |
| `professionSkillMap` | 11924-11938 | ~15 lines | Never imported. Dead code. |
| `professionSpellMap` | 11940-11984 | ~45 lines | Never imported. Dead code. |

**Additional dead**: ~88 lines of profession data never wired into any parser.

### E. Item Data Tables (large, expansion-specific)

Gems and socket bonuses. Huge dicts mapping item IDs to property values. TBC and WotLK each have their own copy.

| Symbol | Lines | Size | Used by |
|---|---|---|---|
| `gemPropertyMap` | 742-1008 | ~267 lines (TBC) | `src/config.py` → ExpansionConfig(1) |
| `gemPropertyMapWotLK` | 1009-1638 | ~630 lines | `src/config.py` → ExpansionConfig(2) |
| `gemIDPropertyMap` | 1639-1895 | ~257 lines (TBC) | `src/config.py` → ExpansionConfig(1) |
| `gemIDPropertyMapWotlk` | 1896-2506 | ~611 lines | `src/config.py` → ExpansionConfig(2) |
| `itemSocketBonusMap` | 2507-3953 | ~1,447 lines (TBC) | `src/config.py` → ExpansionConfig(1) |
| `itemSocketBonusMapWotlk` | 3954-9548 | **~5,595 lines** | `src/config.py` → ExpansionConfig(2) |

These are the single largest consumer of file size. Together they account for ~8,760 lines — 61% of the file.

### F. Suffix & Enchantment Tables

Maps suffix IDs to enchantment slot values for gear quality display.

| Symbol | Lines | Size | Used by |
|---|---|---|---|
| `suffixTable` | 12011-12089 | ~79 lines | `src/items/enchantments.py` |
| `suffixTable2` | 12090-14119 | ~2,030 lines | `src/items/enchantments.py` |

### G. Pet Data

| Symbol | Lines | Size | Used by |
|---|---|---|---|
| `genericPetModelMap` | 11985-12010 | ~26 lines | `src/parsers/pet.py` |

### H. SQL Templates (end of file)

All the string.Template objects for generating INSERT statements. Each expansion gets its own variant where needed.

| Symbol | Lines | Used by |
|---|---|---|
| `pdumpTemplate` | 14123-14143 | `src/output.py` |
| `equipmentTemplate` | 14144-14147 | `src/output.py` |
| `instanceEnchantTemplateWOTLK` | 14148-14150 | `src/output.py` |
| `instanceEnchantTemplateTBC` | 14151-14153 | `src/config.py`, `src/output.py` |
| `instanceEnchantTemplateVan` | 14154-14157 | `src/config.py`, `src/items/enchantments.py` |
| `charactersTemplateWOTLK` | 14158-14160 | `src/config.py` |
| `charactersTemplateTBC` | 14161-14163 | `src/config.py` |
| `charactersTemplateVan` | 14164-14167 | `src/config.py` |
| `skillsTemplate` | 14168-14172 | `src/parsers/skills.py`, `src/parsers/spells.py` |
| `wornTemplate` | 14173-14177 | `src/items/assembly.py` |
| `instanceTemplate` | 14178-14182 | `src/config.py` |
| `instanceTemplateWotLK` | 14183-14187 | `src/config.py` |
| `actionTemplate` | 14188-14191 | `src/config.py` |
| `actionTemplateWotLK` | 14192-14195 | `src/config.py` |
| `petTemplate` | 14196-14199 | `src/config.py` |
| `petTemplateWotLK` | 14200-14203 | `src/config.py` |
| `spellTemplate` | 14204-14207 | `src/parsers/spells.py` |
| `talentTemplate` | 14208-14211 | `src/parsers/talents.py` |
| `factionTemplate` | 14212-14215 | `src/parsers/factions.py` |
| `questTemplate` | 14216-14219 | `src/config.py` |
| `questTemplateWotLK` | 14220-14223 | `src/config.py` |
| `glyphTemplate` | 14224-14227 | `src/parsers/glyphs.py` |
| `achievementTemplate` | 14228-14231 | `src/parsers/achievements.py` |
| `singleMacroTemplate` | 14232-14237 | `src/parsers/macros.py` |

### I. Action & Glyph Mappings

| Symbol | Lines | Size | Used by |
|---|---|---|---|
| `actionMap` | 9549 | 1 line | `src/parsers/actions.py` |
| `glyphMap` | 11531-11894 | ~364 lines | `src/parsers/glyphs.py` |

---

## Size Breakdown

| Category | Lines | % of File | Status |
|---|---|---|---|
| Dead code (A) | ~2,153 | 15.1% | Remove |
| Template utility (B) | 17 | 0.1% | Keep / promote |
| Character identity (C) | ~85 | 0.6% | Group together |
| Skills & professions (D) | ~642 + ~88 dead | 4.5% | Group together, strip dead |
| Item data tables (E) | ~8,760 | 61.5% | By far the largest chunk |
| Suffix/enchant tables (F) | ~2,109 | 14.8% | Group together |
| Pet data (G) | ~26 | 0.2% | Small, can live with character identity |
| SQL templates (H) | ~115 | 0.8% | Keep together — they're all related |
| Action & glyph mappings (I) | ~365 | 2.6% | Group together or with parsers |

---

## Proposed File Split

```
src/
├── constants.py            → thin __init__ / re-exports only (~30 lines)
├── template.py             → Template class (17 lines + docstring)
├── identity.py             → slotMap, slots, races, classes, factions, startPosMap, genericPetModelMap
├── skills.py               → tbcSkillMap, vanillaSkillMap, duplicateSkills, skillmap, ridingSpellMap
├── gems.py                 → gemPropertyMap (TBC+WotLK), gemIDPropertyMap (TBC+Wotlk)
├── socket_bonus.py         → itemSocketBonusMap (TBC+Wotlk)
├── suffixes.py             → suffixTable, suffixTable2
├── glyphs.py               → glyphMap
├── sql_templates.py        → all Template instances
└── actions.py              → actionMap
```

### File details

#### `src/template.py` (~30 lines)

The `Template` class and the `char_guid` it depends on. This is foundational — every SQL template uses it. Making it its own file means no module loads 14K lines just to get string.Template behavior.

```python
from string import Template as _Base

_CHAR_GUID = 500

class Template(_Base):
    ...
```

#### `src/identity.py` (~120 lines)

All the small character-creation lookup tables: slot names→IDs, race/class/faction IDs, starting positions, and pet model map. These are all <50 entries each, stable data that doesn't change between expansions (except startPosMap which is expansion-keyed).

```python
slotMap = {...}
slots = [...]
startPosMap = {...}
factions = {...}
races = {...}
classes = {...}
genericPetModelMap = {...}
```

#### `src/skills.py` (~630 lines)

All skill name→ID mappings plus the class→default-skill map. These are locale-specific and expansion-specific dicts that only `parsers/skills.py` and `parsers/spells.py` reference.

```python
tbcSkillMap = {"enUS": {...}, ...}
vanillaSkillMap = {"enUS": {...}, ...}
duplicateSkills = {...}
skillmap = {...}
ridingSpellMap = {...}
```

#### `src/gems.py` (~1,765 lines)

The four gem property/ID maps. TBC and WotLK each carry their own complete copy because the databases differ. These are ~260-630 lines per table, all pure `{id: value}` dicts. Only imported by `config.py` to feed ExpansionConfig.

```python
gemPropertyMap = {...}          # TBC
gemPropertyMapWotLK = {...}     # WotLK
gemIDPropertyMap = {...}        # TBC
gemIDPropertyMapWotlk = {...}   # WotLK
```

#### `src/socket_bonus.py` (~7,042 lines)

The two socket bonus maps. This is the single largest data blob — especially WotLK at ~5,600 lines. It's a simple `{item_id: bonus_value}` dict. Only imported by `config.py`. Despite being large, it makes sense as its own file because:
- No other module imports it directly
- If you ever want to trim or optimize it, it's self-contained
- Keeping gems and socket bonuses separate avoids a 8.7K-line monolith

```python
itemSocketBonusMap = {...}       # TBC
itemSocketBonusMapWotlk = {...}  # WotLK
```

#### `src/suffixes.py` (~2,109 lines)

The two suffix enchant tables that map quality suffix IDs to enchant slot values. Only used by `items/enchantments.py`.

```python
suffixTable = {...}
suffixTable2 = {...}
```

#### `src/glyphs.py` (~364 lines)

Maps glyph spell IDs to database glyph IDs. Only used by `parsers/glyphs.py`.

```python
glyphMap = {...}
```

#### `src/sql_templates.py` (~115 lines)

All the SQL INSERT template strings. They're all short (1-4 lines each), related, and referenced across many modules. Keeping them together is correct — splitting them would scatter tiny snippets across more files without real benefit.

```python
pdumpTemplate = Template(...)
equipmentTemplate = Template(...)
instanceEnchantTemplateWOTLK = Template(...)
# ... etc.
```

#### `src/actions.py` (~5 lines)

Just `actionMap`. Tiny, but keeping it out of the identity file avoids mixing "character creation data" with "action bar metadata".

```python
actionMap = {"spell": 0, "macro": 64, "item": 128, "companion": 0}
```

#### `src/constants.py` → `__init__.py` (~30 lines)

After the split, `constants.py` becomes a thin re-export hub. Every consumer imports from `src.constants.X` today, so backward compatibility is maintained by re-exporting:

```python
"""Re-exports for backward compatibility."""
from src.template import Template, char_guid
from src.identity import slotMap, slots, startPosMap, factions, races, classes, genericPetModelMap
from src.skills import tbcSkillMap, vanillaSkillMap, duplicateSkills, skillmap, ridingSpellMap
from src.gems import gemPropertyMap, gemPropertyMapWotLK, gemIDPropertyMap, gemIDPropertyMapWotlk
from src.socket_bonus import itemSocketBonusMap, itemSocketBonusMapWotlk
from src.suffixes import suffixTable, suffixTable2
from src.glyphs import glyphMap
from src.sql_templates import (pdumpTemplate, equipmentTemplate, ...)
from src.actions import actionMap

__all__ = [...]
```

---

## Dead Code to Remove

| Item | Lines | Location |
|---|---|---|
| `import os.path`, `import sys` | 2 | L1-2 |
| Mutable state vars (`pet_list` through `class_name`) | 14 | L21-34 |
| `itemguiditr` | 1 | L35 |
| `equip_offset` | 1 | L37 |
| `learned_professions` | 15 | L38-52 |
| `maxSkillMap` | 1 | L99 |
| `talentArray` | ~2,000 | L9551-11530 |
| `professionMap`, `all_prof_skill_ids`, `professionSkillMap`, `professionSpellMap` | ~88 | L11895-11984 |

**Total dead code**: **~2,153 lines** (15.1% of file)

---

## Impact on Existing Imports

Every existing import path stays valid because the `__init__.py` re-exports everything:

| Current import | Still works? |
|---|---|
| `from src.constants import Template, slotMap, classes, ...` | Yes — re-exported from `__init__.py` |
| `from src.config import _exp_config` (which imports gem maps from constants) | Yes — same path through `__init__.py` |

**Zero changes needed in consumer files.** The split is transparent to callers.

---

## Migration Strategy

Given that the data blobs are immutable dicts loaded at module init, migration can happen in one commit:

1. **Remove dead code first** (verify no references with grep — done above). Drops file from 14,238 to ~12,085 lines.
2. **Extract each section into its own file.** Data is copy-paste safe — no logic changes.
3. **Replace `constants.py` with thin `__init__.py` re-export hub.**
4. **Verify imports**: run `python3 -c "from src.parser import parse_file"` and process a test file for each expansion (0, 1, 2).

The key risk is forgetting to re-export something from the new `__init__.py`. Mitigation: every existing import target gets explicitly listed in `__all__`.

---

## After Numbers

| Metric | Before | After |
|---|---|---|
| Total lines in `constants/` package | 14,238 (1 file) | ~10,935 (9 files + __init__.py) |
| Largest file | constants.py (14,238) | socket_bonus.py (7,042) |
| Dead code lines | ~2,153 | 0 |
| Files touched for a gem-related change | 1 (search 14K lines) | `gems.py` (~1,765 lines) |
| Files touched for template changes | 1 (search 14K lines) | `sql_templates.py` (~115 lines) |

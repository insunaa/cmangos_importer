# Parser Module Separation Plan

**Purpose**: Split `src/parser.py` (~942 lines) into focused modules by responsibility, while keeping `src/constants.py` (~14,238 lines) untouched for now. The goal is readable imports, no circular dependencies, and minimal friction for future development.

---

## Current Structure

```
src/
├── parser.py        (~942 lines, 30+ functions/classes)
└── constants.py     (~14,238 lines, data tables + SQL templates)
```

`parser.py` currently mixes concerns: data structures, item logic (gems/enchants/suffixes), slot/bag inventory assembly, per-section parsers (spells, talents, actions, factions, macros, quests, glyphs, achievements, skills), output assembly (pdump writing), and the public entry point.

---

## Proposed Structure

```
src/
├── __init__.py                  # re-export parse_file for backwards compat
├── parser.py                    # thin orchestrator (~100 lines)
├── dataclasses.py               # ParseOutput, ExpansionConfig + factory
├── config.py                    # _EXPAN_CONFIGS map, _exp_config(), module-level constants
├── items/
│   ├── __init__.py              # re-export item helpers
│   ├── normalizer.py            # _normalize_item_fields, _pad_gems, _default_gems
│   ├── enchantments.py          # enchant builder hierarchy + suffix lookup
│   └── assembly.py              # _add_to_itemlists (inventory + instance row assembly)
├── parsers/
│   ├── __init__.py              # re-export all _parse_* functions
│   ├── equipment.py             # _parse_equipment
│   ├── pet.py                   # _parse_pet
│   ├── bags.py                  # _parse_bag_contents
│   ├── spells.py                # _parse_spells
│   ├── talents.py               # _parse_talents
│   ├── actions.py               # _parse_actions
│   ├── factions.py              # _parse_factions
│   ├── macros.py                # _parse_macros, _write_macros
│   ├── quests.py                # _parse_quests
│   ├── glyphs.py                # _parse_glyphs
│   ├── achievements.py          # _parse_achievements
│   └── skills.py                # _parse_char_skills, _add_default_skills
├── output.py                    # _empty_enchant, _fill_equipment_cache, _write_pdump
└── constants.py                 # unchanged (data tables + SQL templates)
```

---

## Module Breakdown

### 1. `src/dataclasses.py` -- Data structures

| Moved from `parser.py` lines | Symbols |
|---|---|
| 119-149, 203-219 | `ExpansionConfig`, `ParseOutput` |

These are pure data classes with no dependencies on other parser internals. Extracting them first removes the biggest structural anchors from `parser.py`.

**Dependencies**: None internal (only stdlib + typing).

---

### 2. `src/config.py` -- Expansion configuration

| Moved from `parser.py` lines | Symbols |
|---|---|
| 152-196, 199-200 | `_EXPAN_CONFIGS`, `_exp_config()` |
| 61-85, 88-115 | Module-level constants (`CHAR_GUID`, `ITEM_GUID_*`, `EQUIPMENT_SLOT_COUNT`, etc.) |

The constants block (GUIDs, slot counts, spell remap IDs, bag defaults, buckles, required fields, equip cache slots) currently lives at the top of `parser.py`. This is the right home for them -- they define *how* parsing works, not *what* data we're looking up.

**Dependencies**: `constants.py` (for template objects), `dataclasses.py` (ExpansionConfig).

---

### 3. `src/items/normalizer.py` -- Item field normalization

| Moved from `parser.py` lines | Symbols |
|---|---|
| 223-224, 227-232, 235-244 | `_default_gems`, `_pad_gems`, `_normalize_item_fields` |

Pure functions that transform raw JSON item dicts into the internal representation (suffix, enchant, gems array, buckle). No side effects.

**Dependencies**: None internal. Can be unit-tested in isolation.

---

### 4. `src/items/enchantments.py` -- Enchantment construction

| Moved from `parser.py` lines | Symbols |
|---|---|
| 247-254, 257-267, 270-277, 280-289, 292-326, 329-350 | `_lookup_suffix_enchants`, `_build_enchantments_vanilla`, `_resolve_socket_bonus`, `_resolve_gem_values`, `_build_enchantments_post_vanilla`, `_build_enchantments` |

This group handles the expansion-branching logic for building item instance enchantment rows. Currently ~100 lines of nested if/elif across 7 functions. Keeping them together makes sense because they form a pipeline: suffix lookup -> gem resolution -> socket bonus -> final SQL row string.

**Dependencies**: `constants.py` (suffixTable, suffixTable2), `config.py` (ExpansionConfig via `_exp_config`).

---

### 5. `src/items/assembly.py` -- Inventory + instance row assembly

| Moved from `parser.py` lines | Symbols |
|---|---|
| 353-393 | `_add_to_itemlists` |

The "write an item to both inventory and instance lists" function. It ties together normalization, enchantments, and GUID incrementing. This is the only item-related function with side effects (mutates `ParseOutput`).

**Dependencies**: `dataclasses.py` (ParseOutput), `config.py` (constants + `_exp_config`), `items/normalizer.py`, `items/enchantments.py`.

---

### 6. `src/parsers/` -- Per-section parsers

Each parser function is small (10-60 lines), takes `(data, output, exp)` and writes into `ParseOutput`. They are independent of each other -- the only shared state is the output accumulator. Splitting them into individual files makes sense because:

- Each maps to a distinct section of the input JSON (`equipment`, `bagContents`, `spells`, etc.)
- Future changes to one section (e.g., bag logic) won't affect others
- Tests can target specific parsers in isolation

#### File assignments

| File | Moved from lines | Functions | Lines | Dependencies |
|---|---|---|---|---|
| `equipment.py` | 397-421 | `_parse_equipment` | ~25 | items/assembly, items/normalizer, config |
| `pet.py` | 425-458 | `_parse_pet` | ~35 | config, constants |
| `bags.py` | 462-523 | `_parse_bag_contents` | ~65 | items/assembly, items/normalizer (`_default_gems`), config |
| `spells.py` | 527-568 | `_parse_spells` | ~45 | config |
| `talents.py` | 572-588 | `_parse_talents` | ~17 | constants only |
| `actions.py` | 592-612 | `_parse_actions` | ~20 | config |
| `factions.py` | 616-625 | `_parse_factions` | ~10 | constants only |
| `macros.py` | 629-655 | `_parse_macros`, `_write_macros` | ~30 | constants (singleMacroTemplate) |
| `quests.py` | 659-667 | `_parse_quests` | ~10 | config |
| `glyphs.py` | 671-686 | `_parse_glyphs` | ~17 | constants only |
| `achievements.py` | 709-722 | `_parse_achievements` | ~15 | stdlib (datetime, time) |
| `skills.py` | 690-706, 726-768 | `_add_default_skills`, `_parse_char_skills` | ~60 | constants (skillmap, skillMaps) |

**Note**: The talent and factions parsers are extremely small (~10-17 lines each). If granularity at this level feels excessive, they could be co-located in a `misc.py` or `simple_parsers.py`. This is a judgment call -- the table above shows the most granular option.

---

### 7. `src/output.py` -- PDump assembly and writing

| Moved from `parser.py` lines | Symbols |
|---|---|
| 772-798, 801-803, 806-876 | `_empty_enchant`, `_fill_equipment_cache`, `_write_pdump` |

This module takes the fully populated `ParseOutput` and assembles the final SQL file. It handles expansion-specific branching for the characters row template and empty enchant fill. It is the last stage of the pipeline -- all parsers have finished by this point.

**Dependencies**: `dataclasses.py` (ParseOutput), `config.py` (`_exp_config`, constants), `constants.py` (templates).

---

### 8. `src/parser.py` -- Thin orchestrator

After extraction, `parser.py` becomes a lightweight entry point:

```python
from src.dataclasses import ParseOutput
from src.config import ...
from src.parsers.equipment import _parse_equipment
from src.parsers.pet import _parse_pet
# ... (one import per parser)
from src.output import _write_pdump


def parse_file(data, exp):
    """Parse a GearExporter JSON and write the character pdump SQL file."""
    output = ParseOutput()
    # validation (lines 883-909) stays here -- it's the public API contract
    # ... player field checks ...

    # orchestration (lines 928-942) stays here -- it defines the pipeline order
    _add_default_skills(...)
    _parse_bag_contents(data, output, exp)        # bags before equipment
    _parse_equipment(data, output, exp, slot_cache)
    _parse_pet(...)
    _parse_spells(...)
    _parse_talents(...)
    _parse_actions(...)
    _parse_factions(...)
    _parse_macros(...)
    _parse_quests(...)
    _parse_glyphs(...)
    _parse_achievements(...)
    _parse_char_skills(...)
    _write_pdump(...)
```

**Target size**: ~100 lines (validation + pipeline ordering). The public API (`parse_file`) remains importable from `src.parser` for backwards compatibility with `main.py`.

---

### 9. `src/__init__.py` -- Package entry point

```python
from src.parser import parse_file
__all__ = ["parse_file"]
```

Ensures `from src.parser import parse_file` in `main.py` continues to work without modification.

---

## Dependency Graph

```
dataclasses.py          <-- no internal deps
config.py               --> dataclasses, constants
items/normalizer.py     <-- no internal deps
items/enchantments.py   --> config, constants
items/assembly.py       --> dataclasses, config, items/normalizer, items/enchantments
parsers/equipment.py    --> items/assembly, items/normalizer, config, constants
parsers/bags.py         --> items/assembly, items/normalizer, config, constants
parsers/pet.py          --> config, constants
parsers/spells.py       --> config, constants
parsers/skills.py       --> constants
parsers/{rest}          --> config, constants (as needed)
output.py               --> dataclasses, config, constants
parser.py               --> dataclasses, config, items/*, parsers/*, output, constants
```

No cycles. Data flows one way: `constants` -> `config` / `dataclasses` -> `items/*` -> `parsers/*` -> `output` -> `parser.py`.

---

## What stays in `constants.py`

Everything. It is a data dump (~14K lines of mappings and SQL templates) that would be painful to split further without adding complexity. The only risk is the mutable state variables (lines 21-53: `pet_list`, `action_list`, etc.) which are currently written but never read back -- they can be cleaned up separately.

If future work warrants splitting constants, natural boundaries are:
- SQL templates (`pdumpTemplate`, `wornTemplate`, etc.) -> `src/templates.py`
- Skill maps (`vanillaSkillMap`, `tbcSkillMap`) -> `src/skill_maps.py`
- Gem/property maps -> `src/gem_data.py`
- Suffix tables -> `src/suffix_data.py`

This is lower priority and not included in this plan.

---

## Migration Order

Recommended order to minimize breakage during incremental migration:

1. **`dataclasses.py`** -- extract first, zero dependency on other parser internals
2. **`config.py`** -- constants + expansion config map (depends only on step 1 + constants)
3. **`items/normalizer.py`** -- pure functions, easy to test in isolation
4. **`items/enchantments.py`** -- depends on step 2
5. **`items/assembly.py`** -- depends on steps 3-4
6. **`parsers/{talents,factions,glyphs,achievements}`** -- smallest, simplest parsers first
7. **`parsers/{spells,actions,quests}`** -- medium complexity
8. **`parsers/skills.py`** -- combines two functions but is self-contained
9. **`parsers/pet.py`** -- depends on config/templates
10. **`parsers/equipment.py`, `parsers/bags.py`** -- most complex, depend on items/*
11. **`output.py`** -- final assembly stage
12. **`parser.py`** -- rewrite as thin orchestrator last
13. **`__init__.py`** -- add re-exports

Each step is a self-contained commit that keeps `main.py` working (via `from src.parser import parse_file`).

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Import path breakage in `main.py` | `__init__.py` re-exports `parse_file`; `src/parser.py` stays importable |
| Circular imports between items and parsers | Dependency graph is strictly DAG -- verified above. Parsers never import from other parsers. |
| Too many small files | The tiny parsers (talents, factions) can be merged into a `simple_parsers.py` if desired. The 12-file split is the maximum granularity; merging any subset is easy. |
| Constants access scattered across modules | All constants are imported from one place (`src.constants`). No new import paths created. |

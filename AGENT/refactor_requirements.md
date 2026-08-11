# Refactor Requirements — `src/parser.py`

## Overview

`parser.py` is a single ~670-line module containing one top-level helper (`_pad_gems`) and one massive function `parse_file` with 14 nested inner functions. The file parses character JSON data into SQL output for Mangos/CMangos emulator imports across three expansions (Vanilla/TBC/WotLK, controlled by the `exp` parameter).

The following sections describe concrete refactor targets, ordered by impact.

---

## 1. Structural Issues

### 1.1 `parse_file` is too large and monolithic
- **Problem:** ~650 lines, 14 nested inner functions, and a flat sequence of calls at the bottom.
- **Goal:** Extract each parsing concern into a standalone module-level function (or class methods). Inner functions exist only to capture closure variables (`data`, `exp`, `slotCache`, etc.) — these should be explicit parameters instead.

### 1.2 Heavy use of `global` declarations
- **Problem:** Inner functions mutate outer-scope globals via `global` statements (`inventory_list`, `instance_list`, `itemguiditr`, `spells`, `skills`, `talents`, `action_list`, `faction_list`, `quests`, `glyphs`, `achievements`, `cskills`, `pet_list`, `class_name`).
- **Specifically flagged globals:** `global skills, class_name` (L29), `global inventory_list, instance_list, itemguiditr` (L78), `global spells, skills` (L355), `global talents` (L390), `global action_list` (L407), `global faction_list` (L432), `global glyphs` (L475), `global achievements` (L489), `global cskills` (L505).
- **Goal:** Replace globals with a data structure (e.g., a simple namespace, `dataclass`, or `dict`) that is passed explicitly between functions. This makes the code testable and removes hidden side effects.

### 1.3 Nested inner functions capture too much closure state
- **Problem:** Every inner function implicitly reads `data`, `exp`, `slotCache`, `char_info`, `char_guid` from the enclosing scope rather than receiving them as arguments.
- **Goal:** Promote to top-level functions with explicit signatures. This also enables unit testing individual parsers in isolation.

---

## 2. Redundant / Repetitive Code Patterns

### 2.1 Expansion-gated template filling (repeated across many functions)
Multiple functions branch on `exp` to pick a different template/class:

| Location         | Pattern                                           |
|------------------|---------------------------------------------------|
| `add_to_itemlists` (L122–221) | `if exp == 0 / elif exp == 1 / elif exp == 2` for enchantments AND instance template |
| `parse_pet` (L276–297)        | `if exp < 2: petTemplate else: petTemplateWotLK` |
| `parse_actions` (L415–426)    | `if exp != 2: actionTemplate else: actionTemplateWotLK` |
| `parse_quests` (L466–469)     | `if exp > 1: questTemplateWotLK else: questTemplate` |
| `write_pdump` (L565–618)      | Giant `if exp == 0 / elif exp == 1 / else` block for version, enchantments, characters_row |

- **Goal:** Consolidate template selection into a strategy or config object keyed by expansion. E.g., a per-expansion config dict that holds references to the correct templates, so callers never branch on `exp` directly — they just look up the right template from the config.

### 2.2 Enchantment building in `add_to_itemlists` (L117–221)
- **Problem:** ~105 lines of deeply nested conditionals with near-identical blocks that differ only in which gem-property map and suffix-table they use. The TBC and WotLK branches share the same pattern: look up suffix → fill template with gem IDs + socket bonus + suffix enchants.
- **Specific repetitions:**
  - L124–136 vs L138–140: Vanilla suffix lookup vs fallback (same structure, `suffixTable` vs `suffixTable2` try order)
  - L145–165: Two nearly identical TBC blocks differing only on whether `matched` has mixed values (socket bonus logic). The gem lookup lines (L147-149 vs L158-160) are duplicated.
  - L176–196: Two nearly identical WotLK blocks differing only on `buckle` value. Gem lookup lines (L178-180 vs L189-191) are duplicated.
- **Goal:** Extract into helper functions like `_build_enchantments_vanilla`, `_build_enchantments_post_vanilla`, or a single generic function that accepts the gem-map and suffix-table as parameters. Eliminate the duplicated gem-ID lookup code.

### 2.3 Instance template filling (L198–221)
- **Problem:** Three near-identical blocks differing only in which template they call and whether `item_suffix` is negated.
- **Goal:** Resolve the right template and suffix sign up-front, then a single fill call.

### 2.4 Suffix / enchant normalization (repeated in equipment + bag parsing)
- **Problem:** The same patterns appear in both `parse_equipment` (L232–233) and `parse_bag_contents` (L332–337):
  ```python
  suffix = str(item.get("suffix", 0)) or "0"
  enchant = str(item.get("enchantId", 0)) or "0"
  raw_gems = item.get("gems")
  gems = _pad_gems(raw_gems) if raw_gems else default_gems
  buckle_val = item.get("buckle")
  buckle = str(buckle_val).lower() if buckle_val is not None else "false"
  ```
- **Goal:** Extract into a helper like `_normalize_item_fields(item)` that returns a dict or named tuple.

### 2.5 `_pad_gems` + default gems duplicated inline
- **Problem:** `[{"id": 0, "matched": False}] * 3` appears in three places: `_pad_gems` (L12), `parse_equipment` (L236), and `parse_bag_contents` (L311).
- **Goal:** Define as a constant or return from `_pad_gems()` with no arguments.

### 2.6 Position unpacking repeated in `write_pdump`
- **Problem:** `start_pos[0]`, `start_pos[1]`, `start_pos[2]`, `start_pos[3]` are used 3+ times (L574–576, L593–595, L613–615, L626–628).
- **Goal:** Unpack once at the top of the function.

### 2.7 Skill lookup duplication (L517–530)
- **Problem:** The logic to resolve `skill_id` for Vanilla and TBC is nearly identical — only the map name and print message differ.
- **Goal:** Extract to a helper that takes `(skillName, skillMap, expansionLabel)` or use a single map-selector variable.

### 2.8 `bagMap` dictionary reconstructed on every call (L79–85)
- **Problem:** Inside `add_to_itemlists`, a literal dict is built fresh on each invocation.
- **Goal:** Move to module-level constant or compute lazily with a helper.

---

## 3. Naming and Convention Issues

### 3.1 Inconsistent naming styles
| Issue | Detail |
|-------|--------|
| Mixed case styles | `slotCache`, `bagMap`, `itemguiditr` (camelCase) vs `char_info`, `action_list`, `pet_health` (snake_case) |
| Abbreviations | `exp` (expansion), `cskills` (character skills?), `bagno` (bag number?) |
| Single-letter vars | `v` in generator expression (L309) |

- **Goal:** Standardize on PEP 8 snake_case for all variables, functions, and parameters. Rename unclear abbreviations.

### 3.2 Misleading parameter name `bagno`
- **Problem:** The default value is `5` and the name suggests "bag number", but the logic at L88 uses it as a threshold: `if bagno > 3`. The intent is ambiguous.
- **Goal:** Rename to something descriptive like `bag_slot_category` or document its purpose clearly.

### 3.3 Misleading variable name `buckle` / inconsistent handling
- **Problem:** In `parse_equipment` it's called `buckle`, in `parse_bag_contents` it's `buckle_val` / `buckle`. The parameter in `add_to_itemlists` is just `buckle` and compared as a string `"false"`.
- **Goal:** Normalize to boolean or consistent string handling.

---

## 4. Magic Numbers and Hardcoded Values

| Line(s)       | Value          | Issue                              | Goal                           |
|---------------|----------------|------------------------------------|--------------------------------|
| L12–L15       | `3`            | Gem count hardcoded everywhere     | Named constant `GEM_SLOTS = 3`  |
| L79–L85       | `10000`, `23`  | Bag/GUID offsets                   | Named constants                |
| L104          | `23`           | Slot offset                        | Named constant                 |
| L222          | `+= 2`         | GUID increment                     | Documented or named            |
| L358, L363, L365 | `34093`, `348700`, `31892`, `348704`, `31801` | Spell ID remapping          | Named constants with comments  |
| L369–L374     | `75`, `150`, `"60"`, `33388`, `33391` | Riding skill thresholds   | Named constants                |
| L448, L452    | `100`, `16777216`, `120` | Macro slot/GUID magic     | Named constants with comments  |
| L564          | `23162`        | Default bag ID                     | Named constant                 |
| L570          | `14156`        | Vanilla default bag ID             | Named constant                 |
| L590, L606    | Enchantment zero-fills            | Repetitive `0` parameters    | Helper or default factory      |

---

## 5. Data Flow and Coupling

### 5.1 Tight coupling to `constants.py` via star import
- **Problem:** `from src.constants import *` pulls an unknown number of symbols into the module namespace, making it impossible to tell which names come from where without reading both files.
- **Goal:** Use explicit imports (`from src.constants import skillmap, classes, races, ...`).

### 5.2 `char_guid` referenced but not defined in this file
- **Problem:** `char_guid` is used in `parse_pet` (L280, L291) and presumably elsewhere but is never assigned inside `parse_file`. It must come from the global scope or `constants.py`.
- **Goal:** Make it an explicit parameter or derive it clearly within the function.

### 5.3 Output accumulators are globals, not return values
- **Problem:** Each parser appends to a global string/buffer (`+=`) rather than returning a value. This makes testing impossible and ordering implicit.
- **Goal:** Each parser should return its output fragment. A coordinator function collects them and passes them to `write_pdump`.

---

## 6. Error Handling and Robustness

### 6.1 No input validation
- **Problem:** Missing keys in `data` or `player` will raise `KeyError` with no context. E.g., `player["name"]`, `data["equipment"]`, etc.
- **Goal:** Add defensive `.get()` calls or validate the input structure early with clear error messages.

### 6.2 Silent skipping without feedback
- **Problem:** Several `continue` statements silently skip items (e.g., unknown slots, action types, macro slots < 100). The user gets no indication that data was dropped.
- **Goal:** Add warnings or logging for skipped entries.

### 6.3 `_pad_gems` mutation bug risk (L12)
- **Problem:** `[{"id": 0, "matched": False}] * 3` creates a list of three references to the **same** dict. If any code mutates one element's dict in-place, all three change. Currently `_pad_gems` replaces references so it's safe, but it's fragile.
- **Goal:** Use a list comprehension: `[{"id": 0, "matched": False} for _ in range(3)]`.

---

## 7. Proposed Target Architecture

After refactoring, the module (or modules) should look like:

```
parser/
├── __init__.py          # Public API: parse_file(...)
├── entry.py             # Top-level parse_file orchestrator
├── models.py            # Dataclasses for parsed output accumulator
├── templates.py         # Per-expansion template strategy/config
├── items.py             # add_to_itemlists, _normalize_item_fields, enchantment builders
├── equipment.py         # parse_equipment
├── bags.py              # parse_bag_contents
├── pet.py               # parse_pet
├── spells.py            # parse_spells
├── talents.py           # parse_talents
├── actions.py           # parse_actions
├── factions.py          # parse_factions
├── macros.py            # parse_macros, write_macros
├── quests.py            # parse_quests
├── glyphs.py            # parse_glyphs
├── achievements.py      # parse_achievements
├── skills.py            # parse_skills
└── output.py            # write_pdump (SQL assembly + file writing)
```

If splitting into multiple files is too large a change, a minimal refactor keeps everything in one file but:

1. Promotes inner functions to module-level with explicit parameters
2. Replaces globals with an accumulator dataclass passed by reference
3. Extracts repeated enchantment/suffix/gem logic into helpers
4. Resolves magic numbers to named constants
5. Fixes the `_pad_gems` list-multiplication issue
6. Standardizes naming to PEP 8

---

## 8. Priority Ranking

| Priority | Item(s)                                      | Rationale                              |
|----------|----------------------------------------------|----------------------------------------|
| **P0**   | §1.2 Globals → accumulator                    | Makes code testable, removes hidden state |
| **P0**   | §6.3 `_pad_gems` mutation bug                 | Fragile and can silently corrupt data    |
| **P1**   | §1.1 / §1.3 Promote inner functions           | Readability and testability             |
| **P1**   | §2.1 Expansion-gated branching                | Single biggest source of repetition     |
| **P1**   | §2.2 Enchantment building redundancy          | ~100 lines of duplicated logic          |
| **P2**   | §4 Magic numbers                              | Maintainability                        |
| **P2**   | §3 Naming conventions                         | Readability                            |
| **P2**   | §2.4 Item field normalization                 | DRY                                    |
| **P3**   | §6 Error handling                             | Robustness                             |
| **P3**   | §5.1 Star import                              | Python best practice                   |

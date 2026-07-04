# Parser Refactor Design — JSON Input Support

## Goal

Modify `src/parser.py` to parse the structured JSON documents produced by the GearExporter WoW addon (schema defined in `REQUIREMENTS.md`) instead of the old flat text format. The parser output (SQL INSERT statements) remains unchanged.

---

## Current State

### Old Input Format
- Flat text file read line-by-line into a list `f`
- Fields encoded as `key=value` or comma-separated within sections delimited by marker strings (`GEAR FROM BAG`, `TALENTS`, `MACROS`, etc.)
- Gems stored as concatenated strings like `"24029:Red"` where the part after `:` is a color name
- Parser uses string splitting, index offsets (`equip_offset`), and section markers to navigate

### New Input Format (JSON)
- Structured JSON with deterministic top-level key order
- Gems are proper objects: `{"id": 24029, "matched": true}`
- Player identity in nested `player` dict
- Equipment keyed by slot name (no redundant `slot` field)
- All arrays use proper JSON arrays

---

## Input Changes

### File Reading
| Aspect | Before | After |
|---|---|---|
| Read method | `open().readlines()` → list of strings | `json.load()` → dict |
| Variable name | `f` (list of lines) | `data` (parsed dict) |
| Navigation | Line indices + string markers | Dict/array access by key |

### Entry Point Signature
- Keep `parse_file(data, exp)` but `data` is now a dict instead of a list of strings
- Alternatively accept both formats for backward compatibility (detect by type)

---

## Mapping: JSON Keys → Parser Functions

| JSON Key | Current Parser Function | Data Transformation |
|---|---|---|
| `player` | `get_char_info()` | Direct field mapping from `data["player"]` dict |
| `equipment` | `parse_slots_equipped()` | Iterate over dict keys (slot names), extract item records |
| `ammo` | Part of equipment scan (slot 0) | Extract from `data.get("ammo", {}).get("id")` |
| `quiver` | Part of hunter pet section | Extract from `data.get("quiver", {})` |
| `pet` | `parse_pet()` | Direct mapping from `data.get("pet", {})` |
| `bagContents` | `parse_bag()` | Iterate array, call `add_to_itemlists` per entry |
| `talents` | Part of `parse_spells()` (talent detection) | Map `talentGroup` + `id` + `rank` to SQL rows |
| `actions` | Part of `parse_spells()` (action parsing) | Direct mapping from array entries |
| `macros` | `parse_macros()` | Direct mapping from array entries |
| `spells` | Part of `parse_spells()` (spell list) | Already a flat number array — minimal change |
| `factions` | Part of `parse_spells()` (faction parsing) | Map `factionID` + `earnedValue` to SQL rows |
| `quests` | `parse_quests()` | Already a flat number array — minimal change |
| `glyphs` | `parse_glyphs()` | Direct mapping from array entries |
| `achievements` | `parse_achievements()` | Direct mapping, compute timestamp from year/month/day |
| `skills` | `parse_skills()` | Map via skill name → skill_id lookup tables |

---

## Detailed Changes Per Function

### `get_char_info()` — Rewrite as dict field extraction
- **Before:** Parses `f[3]`, `f[4]`, etc. using `split("=")`
- **After:** Read from `data["player"]` directly
- Fields: `name`, `class`, `level`, `race`, `gender`, `server`, `expansion`, `gold`, `locale`
- Expansion detection drives template selection (same as before)
- Skills table seeding (armor + weapon skills from `skillmap`) stays the same

### `parse_slots_equipped()` → Rewrite as `parse_equipment(data)`
- **Before:** Iterates slots, searches lines for slot name markers, parses comma-separated fields
- **After:** Iterate over `data["equipment"]` dict directly — keys are slot names, values are `ItemRecord` dicts
- For each item: extract `id`, `suffix`, `unique`, `enchantId`, `gems`, `buckle`
- Use `slotMap` to convert slot name → DB slot ID (already exists in constants)
- Fill `slotCache` same way (needed for `equipmentTemplate`)
- Call `add_to_itemlists()` with parsed values

### `parse_pet()` → Simplify
- **Before:** Searches lines 40+ for "pet" keyword, splits comma-separated string
- **After:** Read from `data.get("pet", {})` directly
- All fields (`name`, `level`, `id`, `family`, `health`, `power`) are already available
- Map `family` to model ID via `genericPetModelMap` (unchanged)

### `parse_bag()` → Rewrite as `parse_bag_contents(data)`
- **Before:** Parses comma-separated lines with `split("=")`, handles two different item formats
- **After:** Iterate over `data["bagContents"]` array directly
- Each entry has: `bag`, `slot`, `id`, `suffix`, `unique`, `count`, `enchantId`, `gems`, `buckle`
- Equipped bag summaries (only `bag` + `id`) need special handling — same as before
- Call `add_to_itemlists()` per entry

### `add_to_itemlists()` — Minimal changes
- The gem handling logic currently splits gems on `:` to get ID and color/match status (e.g., `gems[0].split(":")[0]` for ID, `gems[0].split(":")[1]` for match)
- **Change:** Accept gems as a list of dicts with `id` and `matched` keys instead of strings
- The socket bonus detection checks `"true" in sockets` / `"false" in sockets` — change to check boolean values
- Template filling logic (suffix table lookup, gem property mapping) stays the same

### `parse_spells()` → Split into three functions
The current `parse_spells` does four things: spells, actions, talents, factions. Split for clarity:

1. **`parse_spells(data)`** — Iterate `data["spells"]` (number array). Logic unchanged. Riding spell detection and talent-by-spell lookup stays.
2. **`parse_actions(data)`** — Iterate `data["actions"]`. Map `slot`, `type`, `id` directly. Remove string splitting.
3. **`parse_factions(data)`** — Iterate `data["factions"]`. Map `factionID`, `earnedValue` directly. Remove string splitting.

### `parse_macros()` → Simplify drastically
- **Before:** Two-pass parsing with delimiter detection (`---`), comma-based field splitting
- **After:** Each macro in `data["macros"]` is already a complete dict with `slot`, `name`, `texture`, `body`, `isLocal`
- Filter by slot >= 100 (same as before)
- Fill `singleMacroTemplate` directly

### `parse_quests()` → Trivial change
- Already expects plain IDs. Now reads from `data["quests"]` number array instead of text lines

### `parse_glyphs()` → Direct mapping
- **Before:** Splits on comma for socket/spell fields
- **After:** Read `socket` and `spellID` directly from each dict entry
- Glyph spell ID mapping via `glyphMap` stays the same

### `parse_achievements()` → Direct mapping
- **Before:** Splits comma-separated values
- **After:** Read `id`, `year`, `month`, `day` directly
- Timestamp computation (year + 2000) stays the same

### `parse_skills()` → Minor change
- **Before:** Splits on `;` for name/rank/maxRank from text lines
- **After:** Read `name`, `rank`, `maxRank` from each dict entry
- Skill ID lookup via locale maps (`tbcSkillMap`, `vanillaSkillMap`) stays the same

### `write_pdump()` → No changes needed
- Uses global strings and templates — unaffected by input format change
- `slotCache` still populated correctly by new equipment parser

---

## Concrete Changes Summary

| Function | Change Type | Effort |
|---|---|---|
| Entry point / file reading | Replace `readlines()` with `json.load()`, detect format | Low |
| `get_char_info()` | Full rewrite (dict access vs string splitting) | Medium |
| `parse_slots_equipped()` | Full rewrite (iterate equipment dict) | Medium |
| `add_to_itemlists()` | Adapt gem parameter from string to dict | Medium |
| `parse_pet()` | Simplify (direct dict access) | Low |
| `parse_bag()` | Full rewrite (iterate bagContents array) | Medium |
| `parse_spells()` | Split into spells/actions/factions; simplify input | Medium |
| `parse_macros()` | Simplify drastically (complete dict per macro) | Low |
| `parse_quests()` | Minor (array instead of lines) | Low |
| `parse_glyphs()` | Minor (dict fields instead of string split) | Low |
| `parse_achievements()` | Minor (dict fields instead of string split) | Low |
| `parse_skills()` | Minor (dict fields instead of semicolon split) | Low |
| `write_pdump()` | No change | None |
| `write_macros()` | No change | None |

---

## Constants / Globals to Keep Unchanged

The following in `constants.py` are unaffected:
- All SQL templates (`pdumpTemplate`, `charactersTemplate*`, `instanceTemplate*`, etc.)
- All mapping tables (`slotMap`, `classes`, `races`, `factions`, `skillmap`, `suffixTable*`, `gemPropertyMap*`, `gemIDPropertyMap*`, `itemSocketBonusMap*`, `actionMap`, `talentArray`, `ridingSpellMap`, `genericPetModelMap`, `glyphMap`)
- Global accumulators (`skills`, `spells`, `inventory_list`, etc.)
- The `Template` monkey-patch class

---

## Edge Cases

1. **Nil omission in JSON:** Fields like `suffix`, `enchantId`, `gems` may be absent entirely (not present as null). Use `.get(key, default)` throughout.
2. **Hunter-only fields:** `quiver` and `pet` only exist for hunters — guard with `.get()` 
3. **Empty arrays:** `spells`, `quests`, `talents` etc. may be empty arrays — iterate safely
4. **Expansion gating:** Glyphs and achievements are empty arrays in TBC/WotLK — existing `exp` checks handle this
5. **Bag summary entries:** First items in `bagContents` have only `bag` + `id` — detect by checking for absence of `slot` or `count` keys
6. **Gem array length:** Items may have 1-3 gems; the gem array reflects only non-zero gems

---

## Implementation Order

1. Add JSON loading at entry point, keep `f` as dict
2. Rewrite `get_char_info()` 
3. Rewrite `add_to_itemlists()` to accept gem dicts
4. Rewrite `parse_equipment()` (replaces `parse_slots_equipped()`)
5. Rewrite `parse_bag_contents()` (replaces `parse_bag()`)
6. Split and simplify `parse_spells` → spells, actions, factions
7. Simplify `parse_macros()`, `parse_pet()`, `parse_quests()`, `parse_glyphs()`, `parse_achievements()`, `parse_skills()`
8. Remove `get_all_items()` (no longer needed — sections are top-level keys)
9. Remove `clean()` helper if no longer used
10. Test against existing export files

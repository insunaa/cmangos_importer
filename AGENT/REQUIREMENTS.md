# Gear Exporter — JSON Output Requirements

## Overview

`gear_exporter.lua` is a World of Warcraft addon that scans the player's character state and exports it as **structured, pretty-printed JSON**. The previous version emitted flat `key=value` text lines; this rewrite collects all data into nested Lua tables and serializes them with a dedicated JSON encoder in `json_lib.lua`.

---

## Architecture

| Component | Purpose |
|---|---|
| `scanGear()` | Entry point. Iterates WoW APIs, populates a single `data` table, serializes it to JSON using an explicit root key order, and displays the result in an edit-box frame. |
| `toJson(tbl, keyOrder)` | Global JSON serializer (defined in `json_lib.lua`). Recursively walks Lua tables, emits objects (`{}`) for string-keyed tables and arrays (`[]`) for contiguous 1-based numeric tables. Handles strings (quoted + escaped), numbers, booleans, and nested tables. Nil values are omitted. Accepts an optional `keyOrder` array to enforce deterministic key ordering with pretty-print indentation. |
| `GetItemSplit(itemLink)` | Parses a WoW item link string into a numeric array of fields (item ID, enchant, gems, suffix, unique, etc.). |
| `GetMainFrame(text)` | Creates / reuses the `SimcFrame` dialog — a resizable, movable frame with a scrollable edit box and a single "Okay" button. |
| `convertSlot(raw)` | Maps WoW inventory type constants (e.g. `INVTYPE_HEAD`) to human-readable slot names. |

> **Note:** The old `addPrint()` function was removed entirely — all data now flows through the `data` table.
>
> **Note:** The `toItemRecord(...)` helper from earlier drafts was folded directly into the equipment/bag scan loops — there is no longer a separate function for this.

---

## File Layout

```
GearExporter/
├── GearExporter.toc    # Addon manifest — lists json_lib.lua before gear_exporter.lua
├── json_lib.lua        # Global toJson() serializer (loaded first)
└── gear_exporter.lua   # Main logic: scanGear(), GetMainFrame(), convertSlot()
```

---

## JSON Schema

The root object has the following top-level keys, **always in this order**:

```json
{
  "exporter_version": string,
  "player": PlayerIdentity,
  "equipment": EquipmentMap,
  "ammo": AmmoItem | null,
  "quiver": QuiverItem | null,        // Hunter only
  "pet": PetInfo | null,             // Hunter with active pet only
  "bagContents": BagEntry[],
  "actions": ActionEntry[],
  "macros": MacroEntry[],
  "spells": number[],
  "factions": FactionEntry[],
  "quests": number[],
  "glyphs": GlyphEntry[],
  "achievements": AchievementEntry[],
  "skills": SkillEntry[]
}
```

Key ordering is enforced by passing an explicit `rootKeys` array to `toJson()` — without this, Lua's `pairs()` would yield arbitrary key order.

---

## Data Structures

### PlayerIdentity

| Field | Type | Description |
|---|---|---|
| `name` | string | Character name (`GetUnitName`) |
| `class` | string | Lowercase class string |
| `level` | number | Character level |
| `race` | string | Race name |
| `gender` | number | 1=male, 2=female, 3=neutral (offset by -2 from WoW API) |
| `region` | null | Not available in Classic API — always omitted (nil) |
| `server` | string | Realm name (`GetRealmName`) |
| `role` | string | Hardcoded `"N/A"` |
| `professions` | string | Hardcoded `"N/A"` |
| `talents` | string | Hardcoded `"N/A"` |
| `spec` | string | Hardcoded `"N/A"` |
| `expansion` | number | Expansion level (0=TBC, 1=WotLK, 2=Cata) |
| `gold` | number | Copper amount (`GetMoney`) |
| `locale` | string | Client locale (`GetLocale`) |

### EquipmentMap

An object keyed by slot name. Each value is an **ItemRecord**. The JSON key IS the slot name so there is no redundant `slot` field inside each record.

| Key | Description |
|---|---|
| `head`, `neck`, `shoulder`, `chest`, `waist`, `legs`, `feet`, `wrist`, `hands`, `finger1`, `finger2`, `trinket1`, `trinket2`, `back`, `main_hand`, `off_hand`, `relic` | Standard equipment slots. Only present if an item is equipped in that slot. |

### ItemRecord (equipment items)

| Field | Type | Description |
|---|---|---|
| `id` | number | Item ID |
| `suffix` | number \| null | Suffix ID or null |
| `unique` | number \| null | Unique-equip category bitfield or null |
| `enchantId` | number \| null | Enchantment ID or null |
| `gems` | GemRecord[] \| null | Array of gem records or null |
| `buckle` | boolean \| null | Prismatic buckle state on belt items or null |

### GemRecord

| Field | Type | Description |
|---|---|---|
| `id` | number | Gem item ID |
| `matched` | boolean | Whether the gem color matches the socket color (`gemMatchesSocket` from `C_ItemSocketInfo.GetExistingSocketInfo`) |

### AmmoItem / QuiverItem

| Field | Type | Description |
|---|---|---|
| `id` | number | Item ID of ammo / quiver |

### PetInfo (Hunter only)

| Field | Type | Description |
|---|---|---|
| `name` | string | Pet name |
| `level` | number | Pet level |
| `id` | string | Creature entry ID (6th token from GUID) |
| `family` | string | Family name (e.g. `"Cat"`) |
| `health` | number | Max health |
| `power` | number | Max power/mana/energy |

### BagEntry

| Field | Type | Description |
|---|---|---|
| `bag` | number | Bag index (0=backpack, 1-4=bags, 5+=bank) |
| `slot` | number | Slot within the bag |
| `id` | number | Item ID |
| `suffix` | number \| null | Suffix ID or null |
| `unique` | number \| null | Unique-equip bitfield or null |
| `count` | number | Stack count |
| `enchantId` | number \| null | Enchantment ID or null |
| `gems` | GemRecord[] \| null | Array of gem records or null |
| `buckle` | boolean \| null | Prismatic buckle state or null |

> Equipped bag entries (the first four) contain only `bag` and `id`. Full item rows from iterating bag slots contain all fields. This preserves the original behaviour where bag summaries and detailed listings coexist in one array.

### ActionEntry

| Field | Type | Description |
|---|---|---|
| `slot` | number | Action bar slot (1-120) |
| `type` | string | Action type (`"spell"`, `"item"`, `"macro"`, etc.) |
| `id` | number | Spell/item/macro ID |

### MacroEntry

| Field | Type | Description |
|---|---|---|
| `slot` | number | Macro slot index |
| `name` | string | Macro name |
| `texture` | string | Icon texture path |
| `body` | string | Macro command text |
| `isLocal` | boolean | Whether the macro is character-specific |

### FactionEntry

| Field | Type | Description |
|---|---|---|
| `factionID` | number | Faction group ID |
| `name` | string | Faction name |
| `earnedValue` | number | Current reputation standing value |

### GlyphEntry (Cataclysm only)

| Field | Type | Description |
|---|---|---|
| `socket` | number | Glyph slot index |
| `spellID` | number | Glyph spell ID |

### AchievementEntry (Cataclysm only)

| Field | Type | Description |
|---|---|---|
| `id` | number | Achievement ID |
| `year` | number | Year completed |
| `month` | number | Month completed |
| `day` | number | Day completed |

### SkillEntry

| Field | Type | Description |
|---|---|---|
| `name` | string | Skill line name |
| `rank` | number | Current skill rank |
| `maxRank` | number | Maximum skill rank |

---

## Behavior Notes

- **Nil omission:** The JSON serializer omits keys whose value is `nil`. This keeps the output compact — a bag item without an enchant simply has no `enchantId` key rather than `"enchantId": null`.
- **Deterministic key order:** Root-level keys are serialized in the exact order defined by the `rootKeys` array passed to `toJson()`. Nested objects use default `pairs()` iteration (order not guaranteed, but semantically irrelevant).
- **Pretty printing:** Output is indented with 2-space indentation and one member per line for readability.
- **Expansion gating:** Glyphs and achievements are only populated when `expansion == 2` (Cataclysm). For earlier expansions those arrays are empty.
- **Hunter-specific data:** The `quiver` and `pet` keys only appear for hunters. Pets only appear if one is active.
- **Macro body:** Stored verbatim — commas are safe inside JSON strings, no comma-to-dot replacement needed.
- **Spells / Quests:** Stored as plain number arrays (spell IDs and quest IDs the player has unlocked/completed).
- **Socket info API:** Gem match status uses `C_ItemSocketInfo.GetExistingSocketInfo(j)` which returns `(name, icon, gemMatchesSocket)`. The third return value is a boolean indicating whether the gem color matches its socket.
- **Display frame:** A single resizable DialogBoxFrame with a scrollable edit box. The built-in "Okay" button closes the frame. No additional buttons are present.

---

## Example Output (abbreviated)

```json
{
  "exporter_version": "3.3",
  "player": {
    "name": "Thrall",
    "class": "warrior",
    "level": 80,
    "race": "Orc",
    "gender": 1,
    "server": "Area 52",
    "expansion": 2,
    "locale": "enUS"
  },
  "equipment": {
    "head": {
      "id": 40207,
      "suffix": -128,
      "gems": [
        {"id": 32586, "matched": true},
        {"id": 40037, "matched": false}
      ]
    }
  },

  "spells": [6199, 6544, 6693, ...],
  "bagContents": [
    {"bag": 0, "slot": 3, "id": 12345, "count": 5},
    {"bag": 0, "slot": 7, "id": 67890, "suffix": -42, "enchantId": 2653}
  ],
  ...
}
```

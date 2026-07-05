from __future__ import annotations

import warnings
from typing import Dict

# ---------------------------------------------------------------------------
from src.config import MACRO_GUID_BASE, MACRO_GUID_OFFSET, MACRO_MIN_SLOT
from src.constants import singleMacroTemplate


# ---------------------------------------------------------------------------
def _parse_macros(data: Dict) -> str:
    macro_bodies = ""
    raw_macros = data.get("macros", [])
    for macro in raw_macros:
        slot_num = int(macro["slot"])
        if slot_num < MACRO_MIN_SLOT:
            warnings.warn(
                f"Macro '{macro.get('name', '?')}' in slot {slot_num} "
                f"is below minimum ({MACRO_MIN_SLOT}), skipping."
            )
            continue

        body_lines = macro["body"].replace("@", "target=")
        actual_body = singleMacroTemplate.fill(
            macro_guid=MACRO_GUID_BASE + slot_num - MACRO_GUID_OFFSET,
            macro_body=body_lines,
            macro_name=macro["name"],
        )
        macro_bodies += actual_body

    _write_macros(macro_bodies)
    return macro_bodies


# ---------------------------------------------------------------------------
def _write_macros(macro_file: str) -> None:
    with open("macros-cache.txt", "w") as writer:
        writer.write(macro_file)

from __future__ import annotations

import warnings
from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import slotMap
from src.items.assembly import _add_to_itemlists
from src.items.normalizer import _normalize_item_fields


# ---------------------------------------------------------------------------
def _parse_equipment(
    data: Dict,
    output,
    exp: int,
    slot_cache: Dict[str, int],
) -> None:
    equipment = data.get("equipment", {})
    for slot_name, item in equipment.items():
        if slot_name not in slotMap:
            warnings.warn(f"Unknown equipment slot '{slot_name}', skipping item.")
            continue

        fields = _normalize_item_fields(item)

        _add_to_itemlists(
            output,
            exp,
            slotMap[slot_name],
            item["id"],
            fields["suffix"],
            fields["enchant"],
            fields["gems"],
            fields["buckle"],
        )
        slot_cache[slot_name] = item["id"]

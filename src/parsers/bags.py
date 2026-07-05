from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.config import (
    BAG_EQUIP_SLOT_OFFSET,
    EQUIPMENT_SLOT_COUNT,
    ITEM_GUID_INCREMENT,
    ITEM_GUID_START,
)
from src.items.assembly import _add_to_itemlists
from src.items.normalizer import _default_gems, _normalize_item_fields


# ---------------------------------------------------------------------------
def _parse_bag_contents(
    data: Dict,
    output,
    exp: int,
) -> None:
    bag_entries = data.get("bagContents", [])
    if not bag_entries:
        return

    # First pass: assign deterministic GUIDs to container entries
    container_guid_map = {}
    container_idx = 0
    for item in bag_entries:
        if "count" not in item and "slot" not in item:
            bag_num = int(item["bag"])
            container_guid_map[bag_num] = ITEM_GUID_START + (
                container_idx * ITEM_GUID_INCREMENT
            )
            container_idx += 1

    # Second pass: actually add everything
    for i, item in enumerate(bag_entries):
        if "count" not in item and "slot" not in item:
            slot_id = int(item["bag"]) + BAG_EQUIP_SLOT_OFFSET
            fields = {"suffix": "0", "enchant": "0"}
            fields.update(
                gems=_default_gems(),
                buckle="false",
            )
            _add_to_itemlists(
                output,
                exp,
                slot_id,
                item["id"],
                fields["suffix"],
                fields["enchant"],
                fields["gems"],
                fields["buckle"],
            )
            continue

        bag_num = int(item["bag"])
        if bag_num in container_guid_map:
            inv_bag_id = str(container_guid_map[bag_num])
            slot_id = int(item["slot"]) - 1
        else:
            inv_bag_id = "0"
            slot_id = int(item["slot"]) - 1 + EQUIPMENT_SLOT_COUNT
        fields = _normalize_item_fields(item)

        _add_to_itemlists(
            output,
            exp,
            slot_id,
            item["id"],
            fields["suffix"],
            fields["enchant"],
            fields["gems"],
            fields["buckle"],
            bag_id=inv_bag_id,
            item_count=item.get("count", 1),
        )

from __future__ import annotations

from typing import Dict, List

# ---------------------------------------------------------------------------
from src.config import ITEM_GUID_INCREMENT, _exp_config
from src.items.enchantments import _build_enchantments


# ---------------------------------------------------------------------------
def _add_to_itemlists(
    output,
    exp: int,
    slot_id: int,
    item_entry: str,
    suffix: str,
    enchant: str,
    gems: List[Dict[str, object]],
    buckle: str,
    *,
    bag_id: str = "0",
    item_count: int = 1,
) -> None:
    from src.constants import wornTemplate

    suffix = abs(int(suffix))

    output.inventory_list += wornTemplate.fill(
        slot_id=slot_id,
        item_guid=output.item_guid,
        item_entry=item_entry,
        bag_id=bag_id,
    )

    config = _exp_config(exp)
    matched = [gems[0]["matched"], gems[1]["matched"], gems[2]["matched"]]
    gem_ids = [gems[0]["id"], gems[1]["id"], gems[2]["id"]]

    enchantments = _build_enchantments(
        exp, enchant, str(suffix), matched, int(item_entry), buckle, gem_ids
    )

    effective_suffix = -suffix if config.negate_suffix else suffix

    output.instance_list += config.instance_template.fill(
        item_guid=output.item_guid,
        item_entry=item_entry,
        item_count=item_count,
        item_suffix=effective_suffix,
        enchantments=enchantments,
    )

    output.item_guid += ITEM_GUID_INCREMENT

# BSD 3-Clause License.
#
# Copyright (c) 2025, cmangos_importer contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

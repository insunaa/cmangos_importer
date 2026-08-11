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

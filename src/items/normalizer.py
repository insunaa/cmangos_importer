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

from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
def _default_gems() -> List[Dict[str, object]]:
    return [{"id": 0, "matched": False} for _ in range(3)]


# ---------------------------------------------------------------------------
def _pad_gems(raw_gems: Optional[List[Dict]]) -> List[Dict[str, object]]:
    result = _default_gems()
    for i, gem in enumerate(raw_gems or []):
        if i < 3:
            result[i] = {"id": int(gem["id"]), "matched": bool(gem["matched"])}
    return result


# ---------------------------------------------------------------------------
def _normalize_item_fields(item: Dict) -> Dict[str, str]:
    suffix_raw = item.get("suffix", 0)
    enchant_raw = item.get("enchantId", 0)
    buckle_raw = item.get("buckle")
    return {
        "suffix": str(suffix_raw) if suffix_raw else "0",
        "enchant": str(enchant_raw) if enchant_raw else "0",
        "gems": _pad_gems(item.get("gems")),
        "buckle": str(buckle_raw).lower() if buckle_raw is not None else "false",
    }

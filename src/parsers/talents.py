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

"""Resolve character talents from the exported spell list via the Talent DBC mapping."""

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import talentArray, talentTemplate

# ---------------------------------------------------------------------------
# Pre-build a spell_id -> (talent_id, rank) lookup from talentArray.
_spell_to_talent: dict[int, tuple[int, int]] = {}
for entry in talentArray:
    for rank_key in ("r0", "r1", "r2", "r3", "r4"):
        spell_id = int(entry[rank_key])
        if spell_id != 0:
            _spell_to_talent[spell_id] = (
                int(entry["id"]),
                int(rank_key[1]),  # extract rank number from r0, r1, ... r4
            )


# ---------------------------------------------------------------------------
def _parse_talents(data: Dict, output, exp: int) -> None:
    """Derive talents from the spells list by reverse-lookup against talentArray."""
    if exp < 2:
        return

    raw_spells = set(data.get("spells", []))
    # Collect all matching (talent_id, rank) pairs then keep highest rank per talent.
    best_rank: dict[int, int] = {}
    for spell_id, (talent_id, rank) in _spell_to_talent.items():
        if spell_id not in raw_spells:
            continue
        if talent_id not in best_rank or rank > best_rank[talent_id]:
            best_rank[talent_id] = rank

    for talent_id, rank in sorted(best_rank.items()):
        output.talents += talentTemplate.fill(
            talent_id=talent_id,
            current_rank=rank,
        )

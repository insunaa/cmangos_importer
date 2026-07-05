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

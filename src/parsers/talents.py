from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import talentTemplate


# ---------------------------------------------------------------------------
def _parse_talents(data: Dict, output, exp: int) -> None:
    if exp < 2:
        return

    raw_talents = data.get("talents", [])
    for talent in raw_talents:
        rank = talent["rank"]
        if rank == 0:
            continue
        output.talents += talentTemplate.fill(
            talent_id=talent["id"],
            current_rank=rank,
        )

from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import factionTemplate


# ---------------------------------------------------------------------------
def _parse_factions(data: Dict, output) -> None:
    raw_factions = data.get("factions", [])
    for faction in raw_factions:
        output.faction_list += factionTemplate.fill(
            faction_id=faction["factionID"],
            faction_standing=faction["earnedValue"],
        )

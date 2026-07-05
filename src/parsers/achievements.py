from __future__ import annotations

import datetime
import time
from typing import Dict

# ---------------------------------------------------------------------------
from src.config import ACHIEVEMENT_YEAR_OFFSET
from src.constants import achievementTemplate


# ---------------------------------------------------------------------------
def _parse_achievements(data: Dict, output) -> None:
    raw_achievements = data.get("achievements", [])
    for ach in raw_achievements:
        date_time = datetime.datetime(
            ach["year"] + ACHIEVEMENT_YEAR_OFFSET, ach["month"], ach["day"], 0, 0
        )
        timestamp = time.mktime(date_time.timetuple())
        output.achievements += achievementTemplate.fill(
            achievement_id=ach["id"],
            timestamp=timestamp,
        )

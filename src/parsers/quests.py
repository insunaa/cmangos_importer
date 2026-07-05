from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
from src.config import _exp_config


# ---------------------------------------------------------------------------
def _parse_quests(data: Dict, output, exp: int) -> None:
    config = _exp_config(exp)
    raw_quests = data.get("quests", [])
    for quest_id in raw_quests:
        output.quests += config.quest_template.fill(quest_id=quest_id)

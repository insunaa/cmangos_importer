from __future__ import annotations

import warnings
from typing import Dict

# ---------------------------------------------------------------------------
from src.config import _exp_config
from src.constants import actionMap


# ---------------------------------------------------------------------------
def _parse_actions(data: Dict, output, exp: int) -> None:
    config = _exp_config(exp)
    raw_actions = data.get("actions", [])
    for action in raw_actions:
        action_type_name = action["type"]
        if action_type_name not in actionMap:
            warnings.warn(
                f"Unknown action type '{action_type_name}' "
                f"(action id={action.get('id')}), skipping."
            )
            continue

        output.action_list += config.action_template.fill(
            slot_id=int(action["slot"]) - 1,
            action_id=str(action["id"]),
            action_type=actionMap[action_type_name],
        )

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

from __future__ import annotations

import warnings
from typing import Dict

# ---------------------------------------------------------------------------
from src.constants import glyphMap, glyphTemplate


# ---------------------------------------------------------------------------
def _parse_glyphs(data: Dict, output) -> None:
    raw_glyphs = data.get("glyphs", [])
    for glyph in raw_glyphs:
        glyph_spell = glyph["spellID"]
        if glyph_spell not in glyphMap:
            warnings.warn(
                f"Glyph spell {glyph_spell} not found in glyph map, skipping."
            )
            continue
        output.glyphs += glyphTemplate.fill(
            glyph_slot=glyph["socket"] - 1,
            glyph_id=glyphMap[glyph_spell],
        )

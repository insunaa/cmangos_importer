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

import warnings
from typing import Dict

# ---------------------------------------------------------------------------
from src.config import MACRO_GUID_BASE, MACRO_GUID_OFFSET, MACRO_MIN_SLOT
from src.constants import singleMacroTemplate


# ---------------------------------------------------------------------------
def _parse_macros(data: Dict) -> str:
    macro_bodies = ""
    raw_macros = data.get("macros", [])
    for macro in raw_macros:
        slot_num = int(macro["slot"])
        if slot_num < MACRO_MIN_SLOT:
            warnings.warn(
                f"Macro '{macro.get('name', '?')}' in slot {slot_num} "
                f"is below minimum ({MACRO_MIN_SLOT}), skipping."
            )
            continue

        body_lines = macro["body"].replace("@", "target=")
        actual_body = singleMacroTemplate.fill(
            macro_guid=MACRO_GUID_BASE + slot_num - MACRO_GUID_OFFSET,
            macro_body=body_lines,
            macro_name=macro["name"],
        )
        macro_bodies += actual_body

    _write_macros(macro_bodies)
    return macro_bodies


# ---------------------------------------------------------------------------
def _write_macros(macro_file: str) -> None:
    with open("macros-cache.txt", "w") as writer:
        writer.write(macro_file)

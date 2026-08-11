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

from typing import Dict

# ---------------------------------------------------------------------------
from src.config import CHAR_GUID, DEFAULT_PET_MODEL, _exp_config
from src.constants import classes, genericPetModelMap


# ---------------------------------------------------------------------------
def _parse_pet(
    data: Dict,
    char_class_id: int,
    output,
    exp: int,
) -> None:
    if char_class_id != classes["hunter"]:
        return

    pet_data = data.get("pet")
    if not pet_data:
        return

    config = _exp_config(exp)

    family_name = pet_data.get("family")
    model_id = (
        genericPetModelMap.get(family_name, DEFAULT_PET_MODEL)
        if family_name
        else DEFAULT_PET_MODEL
    )

    pet_list_str = config.pet_template.fill(
        no_char_guid=True,
        pet_entry=str(pet_data["id"]),
        pet_owner=CHAR_GUID,
        pet_name=pet_data["name"],
        pet_level=str(pet_data["level"]),
        pet_model=model_id,
        pet_health=int(pet_data.get("health", 30000)),
        pet_resource=int(pet_data.get("power", 100)),
    )

    output.pet_list = pet_list_str

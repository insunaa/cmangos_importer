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

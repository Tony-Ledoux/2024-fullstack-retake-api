from pydantic import BaseModel
from typing import Any


class UpdatePharmacist(BaseModel):
    pharmacist_id: int = None
    on_holiday: int = None
    morning: list = None
    afternoon: list = None

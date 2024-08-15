from pydantic import BaseModel


class UpdatePharmacist(BaseModel):
    pharmacist_id: int
    on_holiday: int
    availability: str

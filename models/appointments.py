from pydantic import BaseModel


class Appointment(BaseModel):
    date_value: str
    pharmacist_id: int
    time_slot: int
    customer: str

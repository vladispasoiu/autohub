from pydantic import BaseModel
from typing import Optional

class BookingCreate(BaseModel):
    user_id: int
    garage_id: int
    service: Optional[str] = None
    date: str
    time_slot: str

class BookingResponse(BaseModel):
    id: int
    user_id: int
    garage_id: int
    service: Optional[str]
    date: str
    time_slot: str
    status: str

    class Config:
        from_attributes = True
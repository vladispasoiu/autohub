from pydantic import BaseModel
from typing import Optional

class BookingCreate(BaseModel):
    user_id: int
    garage_id: int
    service: Optional[str] = None
    date: str
    time_slot: str
    car_info: Optional[str] = None

class BookingUpdate(BaseModel):
    status: Optional[str] = None

class BookingResponse(BaseModel):
    id: int
    user_id: int
    garage_id: int
    service: Optional[str]
    date: str
    time_slot: str
    status: str
    car_info: Optional[str] = None

    class Config:
        from_attributes = True
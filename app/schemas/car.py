from pydantic import BaseModel
from typing import Optional

class CarCreate(BaseModel):
    brand: str
    model: str
    year: int
    engine: str

class CarUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    engine: Optional[str] = None

class CarResponse(BaseModel):
    id: int
    user_id: int
    brand: str
    model: str
    year: int
    engine: str

    class Config:
        from_attributes = True
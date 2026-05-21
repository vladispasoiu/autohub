from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ServiceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    duration_minutes: Optional[int] = None

    class Config:
        from_attributes = True

class GarageCreate(BaseModel):
    name: str
    owner_name: str
    email: EmailStr
    phone: str
    address: str
    city: str = "Bucharest"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    price_from: Optional[float] = None

class GarageUpdate(BaseModel):
    name: Optional[str] = None
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None
    price_from: Optional[float] = None
    rating: Optional[float] = None
    total_reviews: Optional[int] = None
    is_active: Optional[bool] = None

class GarageResponse(BaseModel):
    id: int
    name: str
    owner_name: str
    email: str
    phone: str
    address: str
    city: str
    latitude: Optional[float]
    longitude: Optional[float]
    description: Optional[str]
    is_active: bool
    is_verified: bool
    rating: float
    total_reviews: int
    price_from: Optional[float]
    services: List[ServiceResponse] = []

    class Config:
        from_attributes = True
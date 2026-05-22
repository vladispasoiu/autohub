from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.service import Service
from pydantic import BaseModel

router = APIRouter(prefix="/services", tags=["Services"])

class ServiceCreate(BaseModel):
    garage_id: int
    name: str
    description: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    duration_minutes: Optional[int] = None

class ServiceUpdate(BaseModel):
    garage_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    duration_minutes: Optional[int] = None

class ServiceResponse(BaseModel):
    id: int
    garage_id: int
    name: str
    description: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    duration_minutes: Optional[int] = None

    class Config:
        from_attributes = True

@router.post("/", response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, service: ServiceUpdate, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in service.dict(exclude_unset=True).items():
        setattr(db_service, key, value)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(db_service)
    db.commit()
    return {"status": "deleted"}

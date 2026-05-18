from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.garage import Garage
from app.schemas.garage import GarageCreate, GarageResponse, GarageUpdate

router = APIRouter(prefix="/garages", tags=["Garages"])

@router.post("/", response_model=GarageResponse)
def register_garage(garage: GarageCreate, db: Session = Depends(get_db)):
    existing = db.query(Garage).filter(Garage.email == garage.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_garage = Garage(**garage.dict())
    db.add(db_garage)
    db.commit()
    db.refresh(db_garage)
    return db_garage

@router.get("/", response_model=List[GarageResponse])
def list_garages(
    city: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Garage).filter(Garage.is_active == True)
    if city:
        query = query.filter(Garage.city.ilike(f"%{city}%"))
    if search:
        query = query.filter(Garage.name.ilike(f"%{search}%"))
    return query.order_by(Garage.rating.desc()).all()
@router.get("/{garage_id}", response_model=GarageResponse)
def get_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage

@router.patch("/{garage_id}", response_model=GarageResponse)
def update_garage(garage_id: int, updates: GarageUpdate, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(garage, key, value)
    db.commit()
    db.refresh(garage)
    return garage

@router.delete("/{garage_id}")
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    db.delete(garage)
    db.commit()
    return {"message": f"Garage {garage_id} deleted"}
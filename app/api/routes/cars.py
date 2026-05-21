from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.car import UserCar
from app.schemas.car import CarCreate, CarUpdate, CarResponse
from app.core.auth import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

router = APIRouter(prefix="/cars", tags=["Cars"])
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalid")
    return int(payload["sub"])

@router.get("/", response_model=List[CarResponse])
def get_my_cars(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return db.query(UserCar).filter(UserCar.user_id == user_id).all()

@router.post("/", response_model=CarResponse)
def add_car(car: CarCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    existing = db.query(UserCar).filter(UserCar.user_id == user_id).count()
    if existing >= 3:
        raise HTTPException(status_code=400, detail="Maxim 3 mașini per cont")
    db_car = UserCar(user_id=user_id, **car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_car = db.query(UserCar).filter(UserCar.id == car_id, UserCar.user_id == user_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Mașina nu a fost găsită")
    for key, value in car.dict(exclude_unset=True).items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car

@router.delete("/{car_id}")
def delete_car(car_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    db_car = db.query(UserCar).filter(UserCar.id == car_id, UserCar.user_id == user_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Mașina nu a fost găsită")
    db.delete(db_car)
    db.commit()
    return {"status": "deleted"}
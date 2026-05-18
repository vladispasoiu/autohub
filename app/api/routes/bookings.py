from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).all()

@router.get("/garage/{garage_id}", response_model=List[BookingResponse])
def get_garage_bookings(garage_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.garage_id == garage_id).order_by(Booking.created_at.desc()).all()
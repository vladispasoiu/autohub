from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    garage_id  = Column(Integer, ForeignKey("garages.id"), nullable=False)
    service    = Column(String(100))
    date       = Column(String(20))
    time_slot  = Column(String(10))
    status     = Column(String(20), default="confirmed")
    car_info   = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user   = relationship("User")
    garage = relationship("Garage")
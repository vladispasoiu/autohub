from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Garage(Base):
    __tablename__ = "garages"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), nullable=False)
    owner_name     = Column(String(100))
    email          = Column(String(100), unique=True, index=True)
    phone          = Column(String(20))
    address        = Column(String(200))
    city           = Column(String(50), default="Bucharest")
    latitude       = Column(Float)
    longitude      = Column(Float)
    description    = Column(Text)
    is_active      = Column(Boolean, default=True)
    is_verified    = Column(Boolean, default=False)
    rating         = Column(Float, default=0.0)
    total_reviews  = Column(Integer, default=0)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), onupdate=func.now())
    services       = relationship("Service", back_populates="garage")
    price_from     = Column(Float, default=0.0)
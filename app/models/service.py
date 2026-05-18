from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Service(Base):
    __tablename__ = "services"

    id          = Column(Integer, primary_key=True, index=True)
    garage_id   = Column(Integer, ForeignKey("garages.id"), nullable=False)
    name        = Column(String(100), nullable=False)
    description = Column(Text)
    price_min   = Column(Float)
    price_max   = Column(Float)
    duration_minutes = Column(Integer)

    garage = relationship("Garage", back_populates="services")
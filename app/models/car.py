from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserCar(Base):
    __tablename__ = "user_cars"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand        = Column(String(100), nullable=False)
    model        = Column(String(100), nullable=False)
    year         = Column(Integer, nullable=False)
    engine       = Column(String(100), nullable=False)  # ex: "2.0 TDI" sau text custom
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cars")
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class GarageRating(Base):
    __tablename__ = "garage_ratings"

    id         = Column(Integer, primary_key=True, index=True)
    garage_id  = Column(Integer, ForeignKey("garages.id", ondelete="CASCADE"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id",   ondelete="CASCADE"), nullable=False)
    score      = Column(Integer, nullable=False)
    comment    = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    garage = relationship("Garage", back_populates="ratings")
    user   = relationship("User",   back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("garage_id", "user_id", name="uq_garage_user_rating"),
    )
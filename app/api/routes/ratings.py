from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.rating import GarageRating
from app.models.garage import Garage

router = APIRouter(prefix="/garages", tags=["Ratings"])

@router.post("/{garage_id}/ratings", status_code=201)
def create_rating(
    garage_id: int,
    user_id: int,
    score: int,
    comment: str = None,
    db: Session = Depends(get_db),
):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    existing = db.query(GarageRating).filter(
        GarageRating.garage_id == garage_id,
        GarageRating.user_id == user_id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="You already rated this garage")

    rating = GarageRating(
        garage_id=garage_id,
        user_id=user_id,
        score=score,
        comment=comment,
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating
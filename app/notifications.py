import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.booking import Booking
from app.models.user import User

def send_push_notification(push_token: str, title: str, body: str):
    httpx.post(
        "https://exp.host/--/exponent-push-notification/v2/push",
        json={
            "to": push_token,
            "title": title,
            "body": body,
            "sound": "default",
        }
    )

def send_booking_reminders():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        # găsim toate programările din următoarele 2-3 ore
        bookings = db.query(Booking).filter(Booking.status == "confirmed").all()
        for booking in bookings:
            user = db.query(User).filter(User.id == booking.user_id).first()
            if user and user.push_token:
                send_push_notification(
                    push_token=user.push_token,
                    title="⏰ Reminder programare",
                    body=f"Ai o programare în 2 ore: {booking.service} la {booking.time_slot}"
                )
    finally:
        db.close()
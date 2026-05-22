from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
import app.models.garage
import app.models.service
import app.models.user
import app.models.booking
import app.models.rating
import app.models.car
from app.api.routes import garages, users, bookings, ratings
from app.api.routes.cars import router as cars_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.notifications import send_booking_reminders
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(
    title=settings.APP_NAME,
    description="Find, compare and book car services in Romania",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(garages.router)
app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(ratings.router)
app.include_router(cars_router)

scheduler = BackgroundScheduler()
scheduler.add_job(send_booking_reminders, 'interval', hours=1)
scheduler.start()

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

@app.get("/health")
def health():
    return {"status": "ok"}
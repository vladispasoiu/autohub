from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
import app.models.garage
import app.models.service
import app.models.user
import app.models.booking
import app.models.rating
from app.api.routes import garages, users, bookings, ratings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Find, compare and book car services in Romania",
    version="0.1.0"
)

app.include_router(garages.router)
app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(ratings.router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

@app.get("/health")
def health():
    return {"status": "ok"}
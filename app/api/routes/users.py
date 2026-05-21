from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, ChangePassword
from app.core.auth import hash_password, verify_password, create_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/change-password")
def change_password(data: ChangePassword, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalid")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or not verify_password(data.current_password, user.password):
        raise HTTPException(status_code=400, detail="Parola curentă e greșită")
    user.password = hash_password(data.new_password)
    db.commit()
    return {"status": "ok"}

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_token({"sub": str(db_user.id), "email": db_user.email})
    return {"access_token": token, "token_type": "bearer", "user": db_user}

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db)):
    return {"message": "Profile endpoint — add token auth here"}

@router.post("/{user_id}/push-token")
def save_push_token(user_id: int, push_token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.push_token = push_token
    db.commit()
    return {"status": "ok"}
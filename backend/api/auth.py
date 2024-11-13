# Endpoints for authentication (register, login)
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBearer
from utils.firebase_utils import verify_id_token, firebase_auth
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from models.user import User
from utils.database import get_db

auth_scheme = HTTPBearer()
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user in Firebase Authentication
    firebase_user = firebase_auth.create_user(email=user.email)

    # Add new user to the database
    db_user = User(uid=firebase_user.uid, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=UserResponse)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    firebase_user = firebase_auth.get_user_by_email(user.email)

    # Fetch user from the database
    db_user = db.query(User).filter(User.uid == firebase_user.uid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


async def get_current_user(token: str = Depends(auth_scheme)):
    id_token = token.credentials
    uid = verify_id_token(id_token)
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return uid

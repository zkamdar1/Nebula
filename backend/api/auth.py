# Endpoints for authentication (register, login)
from fastapi import Depends, HTTPException, APIRouter, Header
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from backend.utils.firebase_utils import verify_id_token
from sqlalchemy.orm import Session
from backend.schemas.user import UserResponse
from backend.models.user import User
from backend.utils.database import get_db

auth_scheme = HTTPBearer()
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

class AuthRequest(BaseModel):
    email: EmailStr

@router.post("/register", response_model=UserResponse)
def register_user(
    auth_request: AuthRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, id_token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    uid = verify_id_token(id_token)
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Check if the user already exists in the database
    existing_user = db.query(User).filter(User.uid == uid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # Add new user to the database
    db_user = User(uid=uid, email=auth_request.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_user(
    auth_request: AuthRequest,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, id_token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    uid = verify_id_token(id_token)
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Check if the user exists in the database
    existing_user = db.query(User).filter(User.uid == uid).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Here, you can implement additional login logic, such as generating JWTs for your own system
    return {"message": "User logged in successfully"}



async def get_current_user(token: str = Depends(auth_scheme)):
    id_token = token.credentials
    uid = verify_id_token(id_token)
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return uid

# Endpoints for authentication (register, login)
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBearer
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

@router.post("/register", response_model=UserResponse)
async def register(idToken: str, email: str, db: Session = Depends(get_db)):
    # Verify the Firebase ID token to retrieve the UID
    uid = verify_id_token(idToken)
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if the user already exists in the database
    existing_user = db.query(User).filter(User.uid == uid).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Add new user to the database
    db_user = User(uid=uid, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



async def get_current_user(token: str = Depends(auth_scheme)):
    id_token = token.credentials
    uid = verify_id_token(id_token)
    if uid is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return uid

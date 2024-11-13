from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass  # Placeholder for additional fields on creation, if any

class UserResponse(UserBase):
    uid: str

    class Config:
        orm_mode = True  # Allows using ORM objects with Pydantic models

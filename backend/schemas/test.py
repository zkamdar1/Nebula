# backend/schemas/test.py
from pydantic import BaseModel
from typing import Optional

class TestCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TestRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

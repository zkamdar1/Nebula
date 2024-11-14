# backend/schemas/project.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = None  # Assuming image URLs are valid HTTP URLs

class ProjectCreate(ProjectBase):
    pass  # Extendable for additional fields in the future

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = None  # Allow updating the image URL

class ProjectResponse(ProjectBase):
    id: str
    user_id: str
    last_accessed: datetime

    class Config:
        orm_mode = True

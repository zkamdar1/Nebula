from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass  # No additional fields on creation, yet extendable

class ProjectUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

class ProjectResponse(ProjectBase):
    id: str
    user_id: str
    last_accessed: datetime

    class Config:
        orm_mode = True

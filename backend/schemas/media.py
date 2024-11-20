from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Literal

class MediaBase(BaseModel):
    media_type: Literal["background", "music", "final"]  # Constrain to valid values
    media_url: str = Field(..., regex=r"^https?://")  # Validate as a valid URL

class MediaCreate(MediaBase):
    pass  # Extendable for additional fields

class MediaUpdate(BaseModel):
    media_url: str = Field(..., regex=r"^https?://")  # Allow updating media URLs

class MediaResponse(MediaBase):
    id: UUID
    project_id: UUID

    class Config:
        orm_mode = True

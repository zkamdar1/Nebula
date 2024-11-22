from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import uuid

from backend.utils.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    media_type = Column(String, nullable=False)
    media_url = Column(String, nullable=False)

    project = relationship("Project", back_populates="media")

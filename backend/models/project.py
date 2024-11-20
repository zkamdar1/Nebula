import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.utils.database import Base
from backend.models.media import Media
from sqlalchemy.sql import func

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)  # Placeholder for project thumbnail URL or asset storage path
    last_accessed = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)

    user = relationship("User", back_populates="project")
    media = relationship("Media", back_populates="project", cascade="all, delete")
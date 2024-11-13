from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.utils.database import Base
import datetime

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    image_url = Column(String)  # Placeholder for project thumbnail URL or asset storage path
    last_accessed = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)

    user = relationship("User", back_populates="projects")

from sqlalchemy import Column, String
from backend.utils.database import Base
from sqlalchemy.orm import relationship
from .project import Project

# Adding a relationship with Project
projects = relationship("Project", back_populates="user")

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)  # Firebase UID as the unique identifier
    email = Column(String, unique=True, index=True)
    created_at = Column(String)

import datetime
from sqlalchemy import Column, DateTime, String
from backend.utils.database import Base
from sqlalchemy.orm import relationship
from .project import Project

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)  # Firebase UID as the unique identifier
    email = Column(String, unique=True, index=True)

    # Adding a relationship with Project
    projects = relationship("Project", back_populates="user")
# backend/utils/models.py

from sqlalchemy import Column, Integer, String
from utils.database import Base

class Test(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

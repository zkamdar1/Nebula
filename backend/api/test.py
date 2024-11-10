# backend/api/test_api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from utils.database import get_db
from models.test import Test
from schemas.test import TestCreate, TestRead

router = APIRouter(
    prefix="/test",
    tags=["test"],
)

@router.post("/", response_model=TestRead)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    db_test = Test(name=test.name, description=test.description)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

@router.get("/", response_model=List[TestRead])
def read_tests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tests = db.query(Test).offset(skip).limit(limit).all()
    return tests

@router.get("/{test_id}", response_model=TestRead)
def read_test(test_id: int, db: Session = Depends(get_db)):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test

@router.put("/{test_id}", response_model=TestRead)
def update_test(test_id: int, test: TestCreate, db: Session = Depends(get_db)):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    db_test.name = test.name
    db_test.description = test.description
    db.commit()
    db.refresh(db_test)
    return db_test

@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(db_test)
    db.commit()
    return {"detail": "Test deleted successfully"}

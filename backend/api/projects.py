# Endpoints for managing projects (create, update, get)
'''
from backend.api import generate
from backend.utils.database import get_db
from sqlalchemy.orm import Session
from backend.utils.models import Project

@router.post("/projects")
async def create_project(title: str, db: Session = Depends(get_db)):
    project = Project(title=title)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
'''
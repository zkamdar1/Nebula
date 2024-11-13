# Endpoints for authentication (register, login)
from typing import List
from uuid import uuid4
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend.utils.database import get_db
from backend.schemas.project import ProjectCreate, ProjectResponse
from backend.models.project import Project
from .auth import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    )

@router.post("/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    new_project = Project(
        id=str(uuid4()),
        title=project.title,
        description=project.description,
        user_id=user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return db.query(Project).filter(Project.user_id == user_id).all()

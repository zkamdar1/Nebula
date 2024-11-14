# backend/routes/projects.py
from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.utils.database import get_db
from backend.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from backend.models.project import Project
from .auth import get_current_user
from datetime import datetime, timezone

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    # Create a new project
    new_project = Project(
        title=project.title,
        description=project.description,
        image_url=project.image_url,
        user_id=user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    # Retrieve projects with pagination
    projects = db.query(Project).filter(Project.user_id == user_id).order_by(Project.last_accessed.desc()).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    # Retrieve a single project by ID
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Update last_accessed
    project.last_accessed = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    # Retrieve the project to update
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Update fields if provided
    if project_update.title is not None:
        project.title = project_update.title
    if project_update.description is not None:
        project.description = project_update.description
    if project_update.image_url is not None:
        project.image_url = project_update.image_url
    
    # Update last_accessed
    project.last_accessed = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    # Retrieve the project to delete
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    db.delete(project)
    db.commit()
    
    return

import boto3
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.utils.database import get_db
from backend.utils.s3 import BUCKET_NAME, s3_client
from backend.models.media import Media
from backend.models.project import Project
from backend.schemas.media import MediaResponse
from .auth import get_current_user
import os
import uuid

router = APIRouter(
    prefix="/media",
    tags=["media"]
)

@router.post("/", response_model=MediaResponse, status_code=201)
async def upload_media(
    project_id: str = Form(...),
    media_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Upload a media file to S3 and store its reference in the database.
    """
    # Validate media type
    if media_type not in ['background_clips', 'music_clips']:
        raise HTTPException(status_code=400, detail="Invalid media type.")

    # Check if the project exists and belongs to the user
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or unauthorized.")

    # Generate S3 path
    file_extension = os.path.splitext(file.filename)[-1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    s3_path = f"projects/{project_id}/{media_type}/{unique_filename}"

   # Upload file to S3
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, s3_path)
        s3_url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_S3_REGION')}.amazonaws.com/{s3_path}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {e}")


    # Save media reference in the database
    media = Media(
        project_id=project_id,
        media_type=media_type,
        media_url=s3_url
    )
    db.add(media)
    db.commit()
    db.refresh(media)

    return media

@router.get("/{project_id}/{media_type}", response_model=list[MediaResponse])
def list_media(
    project_id: str,
    media_type: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    List all media files of a specific type for a project.
    """
    # Validate media type
    if media_type not in ["background", "music", "final"]:
        raise HTTPException(status_code=400, detail="Invalid media type.")

    # Check if the project exists and belongs to the user
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or unauthorized.")

    # Query media files
    media_files = db.query(Media).filter(Media.project_id == project_id, Media.media_type == media_type).all()
    return media_files

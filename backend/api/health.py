from fastapi import APIRouter

router = APIRouter()

# Health check endpoint
@router.get("/")
def health_check():
    return {"message": "Backend is running"}
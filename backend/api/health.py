from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

# Health check endpoint
@router.get("/")
def health_check():
    return {"message": "Backend is running"}
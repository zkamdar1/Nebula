# Endpoint to initiate video generation
from fastapi import APIRouter, HTTPException
from backend.video_generator.full_generation.fullvid import create_video_with_audio_and_subtitles

router = APIRouter(
    prefix="/generate",
    tags=["generate"],
)

@router.post("/generate")
async def generate_video_endpoint():
    try:

        final_video = create_video_with_audio_and_subtitles()

        return {"status": "success", "final_video": final_video}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

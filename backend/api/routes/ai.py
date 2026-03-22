from fastapi import APIRouter, Body
from backend.api.services.ai_service import generate_ai_feedback

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/feedback")
async def ai_feedback(data: dict = Body(...)):
    return await generate_ai_feedback(data)
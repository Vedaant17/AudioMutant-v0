from fastapi import APIRouter, UploadFile, File
from backend.api.services.pipeline_service import start_analysis
from backend.api.services.job_store import get_job

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("/start")
async def start(file: UploadFile = File(...)):
    return await start_analysis(file)


@router.get("/status/{job_id}")
async def status(job_id: str):
    job = get_job(job_id)
    return job or {"error": "Job not found"}


@router.get("/result/{job_id}")
async def result(job_id: str):
    job = get_job(job_id)
    if not job:
        return {"error": "Job not found"}
    return job.get("result")
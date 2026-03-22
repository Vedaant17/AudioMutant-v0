import uuid
import os
import shutil
import asyncio
from backend.engine.main import run_pipeline
from .job_store import create_job, update_job, complete_job

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def start_analysis(file):

    job_id = str(uuid.uuid4())
    create_job(job_id)

    filename = f"{job_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # background task
    asyncio.create_task(run_job(job_id, file_path))

    return {"job_id": job_id}


async def run_job(job_id, file_path):

    loop = asyncio.get_event_loop()

    def progress_callback(p, step):
        update_job(job_id, p, step)

    try:
        result = await loop.run_in_executor(
            None,
            run_pipeline,
            file_path,
            progress_callback
        )

        complete_job(job_id, result)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
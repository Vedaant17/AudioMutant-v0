jobs = {}

def create_job(job_id):
    jobs[job_id] = {
        "status": "processing",
        "progress": 0,
        "step": "Starting...",
        "result": None
    }

def update_job(job_id, progress, step):
    if job_id in jobs:
        jobs[job_id]["progress"] = progress
        jobs[job_id]["step"] = step

def complete_job(job_id, result):
    if job_id in jobs:
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["step"] = "Done"
        jobs[job_id]["result"] = result

def get_job(job_id):
    return jobs.get(job_id, None)
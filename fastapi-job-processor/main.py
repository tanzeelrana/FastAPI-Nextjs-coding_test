from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Job
from schemas import JobCreate, JobResponse, JobStatusUpdate
from crud import create_job, get_jobs, get_job, update_job_status
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Background job processing
def process_job(job_id: int):
    db = SessionLocal()  
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found during background processing")
            return
        if job:
            time.sleep(3)
            job.status = "processing"
            db.commit()
            logger.info(f"Job {job_id} is now processing.")

            time.sleep(3)
            job.status = "completed"
            db.commit()
            logger.info(f"Job {job_id} is now completed.")
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        db.rollback()
    finally:
        db.close()

# Create Job
@app.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job_endpoint(job_data: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if not job_data.asset_id.strip():
        raise HTTPException(status_code=422, detail="Asset ID cannot be empty")

    try:
        job = create_job(db, job_data.asset_id)
        background_tasks.add_task(process_job, job.id)
        logger.info(f"Created job {job.id} with asset ID {job_data.asset_id}")
        return job
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Get all Jobs
@app.get("/jobs", response_model=list[JobResponse])
async def get_jobs_endpoint(db: Session = Depends(get_db)):
    jobs = get_jobs(db)
    if not jobs:
        logger.info("No jobs found.")
    return jobs

# Get Job by ID
@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        logger.warning(f"Job {job_id} not found.")
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Update Job Status
@app.put("/jobs/{job_id}/status", status_code=200)
async def update_job_status_endpoint(job_id: int, status_update: JobStatusUpdate, db: Session = Depends(get_db)):
    if status_update.status not in {"pending", "processing", "completed", "failed"}:
        raise HTTPException(status_code=422, detail="Invalid status value")

    job = update_job_status(db, job_id, status_update.status)
    if job is None:
        logger.warning(f"Job {job_id} not found for status update.")
        raise HTTPException(status_code=404, detail="Job not found")

    logger.info(f"Job {job_id} updated to {status_update.status}.")
    return {"message": "Job status updated successfully", "status": job.status}

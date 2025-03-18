from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Job
from schemas import JobCreate, JobResponse
from crud import create_job, get_jobs, get_job, update_job_status
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend to connect (for development, use "*" or specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
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

# Simulated background job processing
def process_job(job_id: int, db: Session):
    time.sleep(3)
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = "processing"
        db.commit()
        time.sleep(3)
        job.status = "completed"
        db.commit()

# Create Job
@app.post("/jobs", response_model=JobResponse)
async def create_job_endpoint(job_data: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = create_job(db, job_data.asset_id)
    background_tasks.add_task(process_job, job.id, db)
    return job

# Get all Jobs
@app.get("/jobs", response_model=list[JobResponse])
async def get_jobs_endpoint(db: Session = Depends(get_db)):
    return get_jobs(db)

# Get Job by ID
@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_endpoint(job_id: int, db: Session = Depends(get_db)):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Update Job Status
@app.put("/jobs/{job_id}/status", response_model=JobResponse)
async def update_job_status_endpoint(job_id: int, status: str, db: Session = Depends(get_db)):
    job = update_job_status(db, job_id, status)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

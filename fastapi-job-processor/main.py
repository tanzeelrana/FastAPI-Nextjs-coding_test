from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from sqlalchemy import Column, Integer, String, DateTime, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import time

# FastAPI App
app = FastAPI()

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./jobs.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, nullable=False)
    status = Column(Enum("pending", "processing", "completed", "failed", name="status_enum"), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/jobs")
async def create_job(asset_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = Job(asset_id=asset_id, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(process_job, job.id, db)
    return job

@app.get("/jobs")
async def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@app.get("/jobs/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/jobs/{job_id}/status")
async def update_job_status(job_id: int, status: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = status
    db.commit()
    return job

def process_job(job_id: int, db: Session):
    time.sleep(3)
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = "processing"
        db.commit()
        time.sleep(3)
        job.status = "completed"
        db.commit()

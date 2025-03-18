from sqlalchemy.orm import Session
from models import Job

def create_job(db: Session, asset_id: str):
    job = Job(asset_id=asset_id, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_jobs(db: Session):
    return db.query(Job).all()

def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def update_job_status(db: Session, job_id: int, status: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = status
        db.commit()
        return job
    return None

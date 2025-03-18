from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, nullable=False)
    status = Column(Enum("pending", "processing", "completed", "failed", name="status_enum"), default="pending")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

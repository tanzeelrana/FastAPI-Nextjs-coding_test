from pydantic import BaseModel
from datetime import datetime

class JobCreate(BaseModel):
    asset_id: str

class JobResponse(BaseModel):
    id: int
    asset_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

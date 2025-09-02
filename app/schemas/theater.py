from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TheaterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    contact_number: Optional[str] = Field(None, max_length=20)

class TheaterCreate(TheaterBase):
    pass

class TheaterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    contact_number: Optional[str] = Field(None, max_length=20)

class TheaterResponse(TheaterBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class HallBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    theater_id: int = Field(..., gt=0)
    total_rows: int = Field(..., gt=0)

class HallCreate(HallBase):
    pass

class HallUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    total_rows: Optional[int] = Field(None, gt=0)

class HallResponse(HallBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

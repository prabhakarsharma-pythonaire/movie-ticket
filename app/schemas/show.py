from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date, time

class ShowBase(BaseModel):
    movie_id: int = Field(..., gt=0)
    hall_id: int = Field(..., gt=0)
    show_date: date
    start_time: time
    end_time: time
    price_multiplier: float = Field(default=1.0, ge=0.0)
    status: str = Field(default="active", max_length=20)

class ShowCreate(ShowBase):
    pass

class ShowUpdate(BaseModel):
    show_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    price_multiplier: Optional[float] = Field(None, ge=0.0)
    status: Optional[str] = Field(None, max_length=20)

class ShowResponse(ShowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

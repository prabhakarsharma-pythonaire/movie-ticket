from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, time

class BookingBase(BaseModel):
    show_id: int = Field(..., gt=0)
    seat_id: int = Field(..., gt=0)

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    booking_reference: str
    amount_paid: float
    status: str
    booking_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class GroupBookingRequest(BaseModel):
    show_id: int = Field(..., gt=0)
    seat_ids: List[int] = Field(..., min_items=1)
    user_id: int = Field(..., gt=0)

class BookingSuggestion(BaseModel):
    show_id: int
    movie_title: str
    theater_name: str
    hall_name: str
    show_date: date
    start_time: time
    available_seats: List[int]
    total_available: int
    
    class Config:
        from_attributes = True

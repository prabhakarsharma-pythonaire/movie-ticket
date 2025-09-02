from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class SeatBase(BaseModel):
    hall_id: int = Field(..., gt=0)
    row_number: int = Field(..., gt=0)
    seat_number: int = Field(..., gt=0)
    seat_type: str = Field(default="standard", max_length=20)
    is_aisle: bool = Field(default=False)

class SeatCreate(SeatBase):
    pass

class SeatResponse(SeatBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SeatLayoutResponse(BaseModel):
    hall_id: int
    hall_name: str
    total_rows: int
    seats_per_row: Dict[int, int]  # row_number -> number of seats
    booked_seats: List[int]  # list of booked seat IDs
    available_seats: List[int]  # list of available seat IDs
    
    class Config:
        from_attributes = True

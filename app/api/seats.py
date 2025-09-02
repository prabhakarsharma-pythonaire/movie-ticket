from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.database import get_db
from app.models.seat import Seat
from app.models.theater import Hall
from app.schemas.seat import SeatCreate, SeatResponse, SeatLayoutResponse
from sqlalchemy import and_

router = APIRouter(prefix="/seats", tags=["seats"])

@router.post("/", response_model=SeatResponse, status_code=status.HTTP_201_CREATED)
def create_seat(seat: SeatCreate, db: Session = Depends(get_db)):
    """Create a new seat."""
    # Verify hall exists
    hall = db.query(Hall).filter(Hall.id == seat.hall_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    # Check if seat already exists
    existing_seat = db.query(Seat).filter(
        Seat.hall_id == seat.hall_id,
        Seat.row_number == seat.row_number,
        Seat.seat_number == seat.seat_number
    ).first()
    
    if existing_seat:
        raise HTTPException(status_code=400, detail="Seat already exists in this position")
    
    db_seat = Seat(**seat.dict())
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

@router.post("/layout/{hall_id}", response_model=List[SeatResponse], status_code=status.HTTP_201_CREATED)
def create_hall_layout(hall_id: int, seats_per_row: Dict[int, int], db: Session = Depends(get_db)):
    """
    Create seat layout for a hall.
    seats_per_row: Dict where key is row number and value is number of seats in that row
    """
    # Verify hall exists
    hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    # Validate that each row has at least 6 seats (3 columns as per requirement)
    for row_num, num_seats in seats_per_row.items():
        if num_seats < 6:
            raise HTTPException(
                status_code=400, 
                detail=f"Row {row_num} must have at least 6 seats (got {num_seats})"
            )
    
    created_seats = []
    
    for row_num, num_seats in seats_per_row.items():
        for seat_num in range(1, num_seats + 1):
            # Determine if it's an aisle seat (seats 3 and 4 are aisle seats)
            is_aisle = seat_num in [3, 4]
            
            seat = Seat(
                hall_id=hall_id,
                row_number=row_num,
                seat_number=seat_num,
                is_aisle=is_aisle
            )
            db.add(seat)
            created_seats.append(seat)
    
    db.commit()
    
    # Refresh all created seats
    for seat in created_seats:
        db.refresh(seat)
    
    return created_seats

@router.get("/hall/{hall_id}", response_model=List[SeatResponse])
def get_seats_by_hall(hall_id: int, db: Session = Depends(get_db)):
    """Get all seats for a specific hall."""
    seats = db.query(Seat).filter(Seat.hall_id == hall_id).order_by(Seat.row_number, Seat.seat_number).all()
    return seats

@router.get("/layout/{hall_id}", response_model=SeatLayoutResponse)
def get_hall_layout(hall_id: int, db: Session = Depends(get_db)):
    """Get the complete layout of a hall with seat information."""
    # Verify hall exists
    hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    # Get all seats for this hall
    seats = db.query(Seat).filter(Seat.hall_id == hall_id).order_by(Seat.row_number, Seat.seat_number).all()
    
    # Group seats by row
    seats_per_row = {}
    for seat in seats:
        if seat.row_number not in seats_per_row:
            seats_per_row[seat.row_number] = 0
        seats_per_row[seat.row_number] += 1
    
    # Get all bookings for this hall's shows
    from app.models.booking import Booking
    from app.models.show import Show
    
    # Get all shows for this hall
    shows = db.query(Show).filter(Show.hall_id == hall_id).all()
    show_ids = [show.id for show in shows]
    
    # Get booked seats
    booked_seats = []
    if show_ids:
        bookings = db.query(Booking).filter(
            and_(
                Booking.show_id.in_(show_ids),
                Booking.status == "confirmed"
            )
        ).all()
        booked_seats = [booking.seat_id for booking in bookings]
    
    # Get available seats (all seats minus booked seats)
    all_seat_ids = [seat.id for seat in seats]
    available_seats = [seat_id for seat_id in all_seat_ids if seat_id not in booked_seats]
    
    return SeatLayoutResponse(
        hall_id=hall_id,
        hall_name=hall.name,
        total_rows=hall.total_rows,
        seats_per_row=seats_per_row,
        booked_seats=booked_seats,
        available_seats=available_seats
    )

@router.get("/{seat_id}", response_model=SeatResponse)
def get_seat(seat_id: int, db: Session = Depends(get_db)):
    """Get a specific seat by ID."""
    seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat

@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(seat_id: int, db: Session = Depends(get_db)):
    """Delete a seat."""
    db_seat = db.query(Seat).filter(Seat.id == seat_id).first()
    if db_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    db.delete(db_seat)
    db.commit()
    return None

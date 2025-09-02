from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from app.core.database import get_db
from app.models.booking import Booking
from app.models.show import Show
from app.models.movie import Movie
from app.schemas.booking import BookingCreate, BookingResponse, GroupBookingRequest, BookingSuggestion
from app.utils.booking_utils import (
    generate_unique_booking_reference, 
    check_seat_availability, 
    find_consecutive_seats,
    find_alternative_bookings,
    calculate_booking_amount,
    validate_seats_in_same_show
)

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a single booking."""
    # Check seat availability
    is_available, unavailable_seats = check_seat_availability(db, booking.show_id, [booking.seat_id])
    
    if not is_available:
        raise HTTPException(
            status_code=400, 
            detail=f"Seat {booking.seat_id} is not available. Unavailable seats: {unavailable_seats}"
        )
    
    # Validate seat belongs to the show's hall
    if not validate_seats_in_same_show(db, booking.show_id, [booking.seat_id]):
        raise HTTPException(status_code=400, detail="Seat does not belong to this show's hall")
    
    # Calculate amount
    amount = calculate_booking_amount(db, booking.show_id, 1)
    
    # Create booking
    db_booking = Booking(
        user_id=user_id,
        show_id=booking.show_id,
        seat_id=booking.seat_id,
        booking_reference=generate_unique_booking_reference(db),
        amount_paid=amount
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    return db_booking

@router.post("/group", response_model=List[BookingResponse], status_code=status.HTTP_201_CREATED)
def create_group_booking(group_booking: GroupBookingRequest, db: Session = Depends(get_db)):
    """Create a group booking for multiple seats together."""
    try:
        # Validate all seats belong to the same show
        if not validate_seats_in_same_show(db, group_booking.show_id, group_booking.seat_ids):
            raise HTTPException(status_code=400, detail="All seats must belong to the same show")
        
        # Check seat availability
        is_available, unavailable_seats = check_seat_availability(db, group_booking.show_id, group_booking.seat_ids)
        
        if not is_available:
            # Find alternative booking options
            show = db.query(Show).filter(Show.id == group_booking.show_id).first()
            if show:
                alternatives = find_alternative_bookings(
                    db, 
                    show.movie_id, 
                    len(group_booking.seat_ids),
                    show.show_date
                )
                
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": f"Requested seats are not available. Unavailable seats: {unavailable_seats}",
                        "alternatives": alternatives
                    }
                )
            else:
                raise HTTPException(status_code=400, detail="Show not found")
        
        # Calculate total amount
        total_amount = calculate_booking_amount(db, group_booking.show_id, len(group_booking.seat_ids))
        
        # Create bookings for all seats
        created_bookings = []
        
        for seat_id in group_booking.seat_ids:
            # Generate unique reference for each booking
            booking_reference = generate_unique_booking_reference(db)
            
            db_booking = Booking(
                user_id=group_booking.user_id,
                show_id=group_booking.show_id,
                seat_id=seat_id,
                booking_reference=booking_reference,
                amount_paid=total_amount / len(group_booking.seat_ids)  # Split amount equally
            )
            db.add(db_booking)
            created_bookings.append(db_booking)
        
        db.commit()
        
        # Refresh all bookings
        for booking in created_bookings:
            db.refresh(booking)
        
        return created_bookings
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/group/consecutive", response_model=List[BookingResponse], status_code=status.HTTP_201_CREATED)
def create_consecutive_group_booking(show_id: int, num_seats: int, user_id: int, db: Session = Depends(get_db)):
    """Find and book consecutive seats for a group."""
    try:
        # Find consecutive seats
        consecutive_seats = find_consecutive_seats(db, show_id, num_seats)
        
        if not consecutive_seats:
            # Find alternative booking options
            show = db.query(Show).filter(Show.id == show_id).first()
            if show:
                alternatives = find_alternative_bookings(db, show.movie_id, num_seats, show.show_date)
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": f"No consecutive seats available for {num_seats} people",
                        "alternatives": alternatives
                    }
                )
            else:
                raise HTTPException(status_code=400, detail="Show not found")
        
        # Create group booking with consecutive seats
        group_booking = GroupBookingRequest(
            show_id=show_id,
            seat_ids=consecutive_seats,
            user_id=user_id
        )
        
        return create_group_booking(group_booking, db)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/alternatives/{movie_id}", response_model=List[BookingSuggestion])
def get_alternative_bookings(movie_id: int, num_seats: int, db: Session = Depends(get_db)):
    """Get alternative booking options for a movie."""
    alternatives = find_alternative_bookings(db, movie_id, num_seats)
    return alternatives

@router.get("/", response_model=List[BookingResponse])
def get_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bookings with pagination."""
    bookings = db.query(Booking).offset(skip).limit(limit).all()
    return bookings

@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a specific user."""
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return bookings

@router.get("/show/{show_id}", response_model=List[BookingResponse])
def get_show_bookings(show_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a specific show."""
    bookings = db.query(Booking).filter(Booking.show_id == show_id).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancel a booking."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    
    return booking

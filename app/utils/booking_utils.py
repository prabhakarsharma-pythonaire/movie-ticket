import uuid
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models import Show, Seat, Booking, Movie, Theater, Hall
from app.schemas.booking import BookingSuggestion
from datetime import datetime, timedelta

def generate_unique_booking_reference(db: Session) -> str:
    """Generate a unique booking reference that doesn't exist in the database."""
    from app.models.booking import Booking
    import time
    import uuid
    import random
    
    max_attempts = 20
    
    for attempt in range(max_attempts):
        # Add a small delay to ensure uniqueness
        if attempt > 0:
            time.sleep(0.001)  # 1 millisecond delay
        
        # Method 1: UUID + timestamp + random
        if attempt < 10:
            unique_id = str(uuid.uuid4()).replace('-', '')[:12].upper()
            timestamp = int(time.time() * 1000000)  # Microseconds
            random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
            reference = f"BK{timestamp}{unique_id}{random_chars}"
        
        # Method 2: Nanosecond timestamp + longer random string
        elif attempt < 15:
            timestamp = int(time.time() * 1000000000)  # Nanoseconds
            random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=15))
            reference = f"BK{timestamp}{random_chars}"
        
        # Method 3: Maximum uniqueness approach
        else:
            timestamp = int(time.time() * 1000000000000)  # Picoseconds
            random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))
            reference = f"BK{timestamp}{random_chars}"
        
        # Check if this reference already exists
        existing = db.query(Booking).filter(Booking.booking_reference == reference).first()
        if not existing:
            return reference
    
    # If we still can't generate a unique one, use a completely different approach
    import hashlib
    timestamp = int(time.time() * 1000000000000000)  # Femtoseconds
    random_data = str(uuid.uuid4()) + str(random.random()) + str(time.time())
    hash_object = hashlib.md5(random_data.encode())
    hash_hex = hash_object.hexdigest().upper()[:20]
    return f"BK{timestamp}{hash_hex}"

def generate_booking_reference() -> str:
    """Generate a unique booking reference."""
    import time
    import random
    
    # Get current timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    
    # Generate random string
    random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    
    # Combine timestamp and random string
    reference = f"BK{timestamp}{random_chars}"
    
    return reference

def check_seat_availability(db: Session, show_id: int, seat_ids: List[int]) -> Tuple[bool, List[int]]:
    """
    Check if seats are available for booking.
    Returns (is_available, unavailable_seats)
    """
    # Get existing bookings for this show and seats
    existing_bookings = db.query(Booking).filter(
        and_(
            Booking.show_id == show_id,
            Booking.seat_id.in_(seat_ids),
            Booking.status == "confirmed"
        )
    ).all()
    
    unavailable_seats = [booking.seat_id for booking in existing_bookings]
    is_available = len(unavailable_seats) == 0
    
    return is_available, unavailable_seats

def find_consecutive_seats(db: Session, show_id: int, num_seats: int) -> List[int]:
    """
    Find consecutive available seats for a group booking.
    Returns list of seat IDs if found, empty list otherwise.
    """
    # Get all seats for this show's hall
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        return []
    
    # Get all seats in the hall, ordered by row and seat number
    hall_seats = db.query(Seat).filter(Seat.hall_id == show.hall_id).order_by(
        Seat.row_number, Seat.seat_number
    ).all()
    
    # Get booked seats for this show
    booked_seat_ids = set()
    bookings = db.query(Booking).filter(
        and_(
            Booking.show_id == show_id,
            Booking.status == "confirmed"
        )
    ).all()
    booked_seat_ids = {booking.seat_id for booking in bookings}
    
    # Group seats by row
    seats_by_row = {}
    for seat in hall_seats:
        if seat.row_number not in seats_by_row:
            seats_by_row[seat.row_number] = []
        seats_by_row[seat.row_number].append(seat)
    
    # Find consecutive seats in each row
    for row_num, row_seats in seats_by_row.items():
        # Sort seats by seat number within the row
        row_seats.sort(key=lambda x: x.seat_number)
        
        # Get available seats in this row
        available_seats = [seat for seat in row_seats if seat.id not in booked_seat_ids]
        
        if len(available_seats) >= num_seats:
            # Check for consecutive seats by seat number
            for i in range(len(available_seats) - num_seats + 1):
                consecutive_seats = available_seats[i:i + num_seats]
                
                # Check if these seats are actually consecutive by seat number
                seat_numbers = [seat.seat_number for seat in consecutive_seats]
                if seat_numbers == list(range(seat_numbers[0], seat_numbers[0] + num_seats)):
                    seat_ids = [seat.id for seat in consecutive_seats]
                    
                    # Verify these seats are still available (double-check)
                    is_available, _ = check_seat_availability(db, show_id, seat_ids)
                    if is_available:
                        return seat_ids
    
    return []

def find_alternative_bookings(db: Session, movie_id: int, num_seats: int, 
                            preferred_date: Optional[datetime] = None) -> List[BookingSuggestion]:
    """
    Find alternative booking options when requested seats are not available.
    """
    suggestions = []
    
    # Get all shows for this movie
    shows = db.query(Show).filter(
        and_(
            Show.movie_id == movie_id,
            Show.status == "active",
            Show.show_date >= datetime.now().date()
        )
    ).order_by(Show.show_date, Show.start_time).all()
    
    for show in shows:
        # Skip if it's the same show that was already tried
        if preferred_date and show.show_date == preferred_date.date():
            continue
            
        consecutive_seats = find_consecutive_seats(db, show.id, num_seats)
        if consecutive_seats:
            # Get movie and theater details
            movie = db.query(Movie).filter(Movie.id == movie_id).first()
            hall = db.query(Hall).filter(Hall.id == show.hall_id).first()
            theater = db.query(Theater).filter(Theater.id == hall.theater_id).first()
            
            suggestion = BookingSuggestion(
                show_id=show.id,
                movie_title=movie.title,
                theater_name=theater.name,
                hall_name=hall.name,
                show_date=show.show_date,
                start_time=show.start_time,
                available_seats=consecutive_seats,
                total_available=len(consecutive_seats)
            )
            suggestions.append(suggestion)
    
    return suggestions

def calculate_booking_amount(db: Session, show_id: int, num_seats: int) -> float:
    """Calculate the total amount for booking."""
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        return 0.0
    
    movie = db.query(Movie).filter(Movie.id == show.movie_id).first()
    if not movie:
        return 0.0
    
    base_price = movie.base_price
    price_multiplier = show.price_multiplier
    total_amount = base_price * price_multiplier * num_seats
    
    return round(total_amount, 2)

def validate_seats_in_same_show(db: Session, show_id: int, seat_ids: List[int]) -> bool:
    """Validate that all seats belong to the same show's hall."""
    if not seat_ids:
        return False
    
    show = db.query(Show).filter(Show.id == show_id).first()
    if not show:
        return False
    
    # Check if all seats belong to the same hall
    seats = db.query(Seat).filter(Seat.id.in_(seat_ids)).all()
    for seat in seats:
        if seat.hall_id != show.hall_id:
            return False
    
    return True

#!/usr/bin/env python3
"""
Demo script for the Movie Booking System API
Showcases all key features including group booking and alternative suggestions
"""

import requests
import json
from datetime import datetime, date, time

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*50}")
    print(f"🎬 {title}")
    print(f"{'='*50}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def demo_basic_crud():
    """Demo basic CRUD operations"""
    print_section("Basic CRUD Operations")
    
    # Create a movie
    movie_data = {
        "title": "Inception",
        "description": "A thief who steals corporate secrets through dream-sharing technology",
        "duration_minutes": 148,
        "genre": "Sci-Fi",
        "language": "English",
        "base_price": 15.00
    }
    
    response = requests.post(f"{BASE_URL}/movies/", json=movie_data)
    if response.status_code == 201:
        movie_id = response.json()["id"]
        print_success(f"Created movie: {movie_data['title']} (ID: {movie_id})")
    else:
        print_error(f"Failed to create movie: {response.text}")
        return None
    
    # Create a theater
    theater_data = {
        "name": "Multiplex Central",
        "address": "456 Entertainment Ave, Downtown",
        "city": "Mumbai",
        "state": "Maharashtra",
        "contact_number": "555-0456"
    }
    
    response = requests.post(f"{BASE_URL}/theaters/", json=theater_data)
    if response.status_code == 201:
        theater_id = response.json()["id"]
        print_success(f"Created theater: {theater_data['name']} (ID: {theater_id})")
    else:
        print_error(f"Failed to create theater: {response.text}")
        return None
    
    # Create a hall
    hall_data = {
        "name": "Premium Hall 1",
        "theater_id": theater_id,
        "total_rows": 8
    }
    
    response = requests.post(f"{BASE_URL}/halls/", json=hall_data)
    if response.status_code == 201:
        hall_id = response.json()["id"]
        print_success(f"Created hall: {hall_data['name']} (ID: {hall_id})")
    else:
        print_error(f"Failed to create hall: {response.text}")
        return None
    
    return movie_id, theater_id, hall_id

def demo_seat_layout(hall_id):
    """Demo seat layout creation"""
    print_section("Seat Layout Management")
    
    # Create flexible seat layout (different seats per row)
    seats_per_row = {
        1: 10,  # Row 1: 10 seats
        2: 8,   # Row 2: 8 seats
        3: 12,  # Row 3: 12 seats
        4: 6,   # Row 4: 6 seats (minimum)
        5: 9,   # Row 5: 9 seats
        6: 7,   # Row 6: 7 seats
        7: 11,  # Row 7: 11 seats
        8: 8    # Row 8: 8 seats
    }
    
    response = requests.post(f"{BASE_URL}/seats/layout/{hall_id}", json=seats_per_row)
    if response.status_code == 201:
        seats = response.json()
        print_success(f"Created {len(seats)} seats across {len(seats_per_row)} rows")
        print(f"   Row configuration: {seats_per_row}")
    else:
        print_error(f"Failed to create seat layout: {response.text}")
        return None
    
    # Get hall layout
    response = requests.get(f"{BASE_URL}/seats/layout/{hall_id}")
    if response.status_code == 200:
        layout = response.json()
        print_success(f"Hall layout retrieved:")
        print(f"   Total rows: {layout['total_rows']}")
        print(f"   Seats per row: {layout['seats_per_row']}")
        print(f"   Available seats: {len(layout['available_seats'])}")
        return layout['available_seats']
    else:
        print_error(f"Failed to get hall layout: {response.text}")
        return None

def demo_show_creation(movie_id, hall_id):
    """Demo show creation"""
    print_section("Show Management")
    
    # Create multiple shows for the same movie
    shows_data = [
        {
            "movie_id": movie_id,
            "hall_id": hall_id,
            "show_date": date.today().isoformat(),
            "start_time": "14:00:00",
            "end_time": "16:28:00",
            "price_multiplier": 1.0,
            "status": "active"
        },
        {
            "movie_id": movie_id,
            "hall_id": hall_id,
            "show_date": date.today().isoformat(),
            "start_time": "18:00:00",
            "end_time": "20:28:00",
            "price_multiplier": 1.2,  # Premium pricing
            "status": "active"
        }
    ]
    
    show_ids = []
    for i, show_data in enumerate(shows_data):
        response = requests.post(f"{BASE_URL}/shows/", json=show_data)
        if response.status_code == 201:
            show_id = response.json()["id"]
            show_ids.append(show_id)
            print_success(f"Created show {i+1}: {show_data['start_time']} (ID: {show_id})")
        else:
            print_error(f"Failed to create show {i+1}: {response.text}")
    
    return show_ids

def demo_user_creation():
    """Demo user creation"""
    print_section("User Management")
    
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "securepass123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 201:
        user_id = response.json()["id"]
        print_success(f"Created user: {user_data['username']} (ID: {user_id})")
        return user_id
    else:
        print_error(f"Failed to create user: {response.text}")
        return None

def demo_single_booking(user_id, show_id, available_seats):
    """Demo single booking"""
    print_section("Single Booking")
    
    if not available_seats:
        print_error("No available seats for booking")
        return None
    
    seat_id = available_seats[0]
    booking_data = {
        "show_id": show_id,
        "seat_id": seat_id
    }
    
    response = requests.post(f"{BASE_URL}/bookings/?user_id={user_id}", json=booking_data)
    if response.status_code == 201:
        booking = response.json()
        print_success(f"Single booking created:")
        print(f"   Booking ID: {booking['id']}")
        print(f"   Reference: {booking['booking_reference']}")
        print(f"   Amount: ${booking['amount_paid']}")
        print(f"   Seat: {booking['seat_id']}")
        return booking['id']
    else:
        print_error(f"Failed to create single booking: {response.text}")
        return None

def demo_group_booking(user_id, show_id, available_seats):
    """Demo group booking"""
    print_section("Group Booking")
    
    if len(available_seats) < 4:
        print_error("Not enough available seats for group booking")
        return None
    
    # Book 4 seats together
    seat_ids = available_seats[1:5]  # Skip the first seat (already booked)
    group_booking_data = {
        "show_id": show_id,
        "seat_ids": seat_ids,
        "user_id": user_id
    }
    
    response = requests.post(f"{BASE_URL}/bookings/group", json=group_booking_data)
    if response.status_code == 201:
        bookings = response.json()
        print_success(f"Group booking created for {len(bookings)} seats:")
        print(f"   Booking Reference: {bookings[0]['booking_reference']}")
        print(f"   Total Amount: ${sum(b['amount_paid'] for b in bookings)}")
        print(f"   Seats: {[b['seat_id'] for b in bookings]}")
        return [b['id'] for b in bookings]
    else:
        print_error(f"Failed to create group booking: {response.text}")
        return None

def demo_consecutive_booking(user_id, show_id):
    """Demo consecutive seat booking"""
    print_section("Consecutive Seat Booking")
    
    # Try to book 3 consecutive seats
    response = requests.post(f"{BASE_URL}/bookings/group/consecutive?show_id={show_id}&num_seats=3&user_id={user_id}")
    if response.status_code == 201:
        bookings = response.json()
        print_success(f"Consecutive booking created for {len(bookings)} seats:")
        print(f"   Booking Reference: {bookings[0]['booking_reference']}")
        print(f"   Seats: {[b['seat_id'] for b in bookings]}")
        return [b['id'] for b in bookings]
    else:
        print_error(f"Failed to create consecutive booking: {response.text}")
        return None

def demo_alternative_suggestions(movie_id):
    """Demo alternative booking suggestions"""
    print_section("Alternative Booking Suggestions")
    
    # Get alternative suggestions for 4 people
    response = requests.get(f"{BASE_URL}/bookings/alternatives/{movie_id}?num_seats=4")
    if response.status_code == 200:
        alternatives = response.json()
        if alternatives:
            print_success(f"Found {len(alternatives)} alternative options:")
            for i, alt in enumerate(alternatives[:3]):  # Show first 3
                print(f"   Option {i+1}:")
                print(f"     Show: {alt['movie_title']}")
                print(f"     Theater: {alt['theater_name']}")
                print(f"     Time: {alt['start_time']}")
                print(f"     Available seats: {alt['total_available']}")
        else:
            print("No alternative suggestions available")
    else:
        print_error(f"Failed to get alternatives: {response.text}")

def demo_booking_management(user_id):
    """Demo booking management features"""
    print_section("Booking Management")
    
    # Get user's bookings
    response = requests.get(f"{BASE_URL}/bookings/user/{user_id}")
    if response.status_code == 200:
        bookings = response.json()
        print_success(f"User has {len(bookings)} bookings:")
        for booking in bookings:
            print(f"   Booking {booking['id']}: Seat {booking['seat_id']}, Status: {booking['status']}")
        
        # Cancel the first booking if available
        if bookings:
            booking_id = bookings[0]['id']
            cancel_response = requests.put(f"{BASE_URL}/bookings/{booking_id}/cancel")
            if cancel_response.status_code == 200:
                print_success(f"Cancelled booking {booking_id}")
            else:
                print_error(f"Failed to cancel booking: {cancel_response.text}")
    else:
        print_error(f"Failed to get user bookings: {response.text}")

def main():
    """Run the complete demo"""
    print("🎬 Movie Booking System - Complete Demo")
    print("=" * 60)
    
    try:
        # Basic CRUD operations
        result = demo_basic_crud()
        if not result:
            print_error("Failed to set up basic entities")
            return
        movie_id, theater_id, hall_id = result
        
        # Seat layout
        available_seats = demo_seat_layout(hall_id)
        if not available_seats:
            print_error("Failed to create seat layout")
            return
        
        # Show creation
        show_ids = demo_show_creation(movie_id, hall_id)
        if not show_ids:
            print_error("Failed to create shows")
            return
        
        # User creation
        user_id = demo_user_creation()
        if not user_id:
            print_error("Failed to create user")
            return
        
        # Booking demonstrations
        demo_single_booking(user_id, show_ids[0], available_seats)
        demo_group_booking(user_id, show_ids[0], available_seats)
        demo_consecutive_booking(user_id, show_ids[1])
        
        # Alternative suggestions
        demo_alternative_suggestions(movie_id)
        
        # Booking management
        demo_booking_management(user_id)
        
        print_section("Demo Complete")
        print_success("All features demonstrated successfully!")
        print(f"📖 API Documentation: http://localhost:8000/docs")
        print(f"🔗 API Base URL: http://localhost:8000/api/v1")
        
    except Exception as e:
        print_error(f"Demo failed with error: {str(e)}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for the Movie Booking System API
"""

import requests
import json
from datetime import datetime, date, time

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def test_movie_creation():
    """Test creating a movie"""
    print("Testing movie creation...")
    
    movie_data = {
        "title": "The Avengers",
        "description": "Earth's mightiest heroes assemble",
        "duration_minutes": 143,
        "genre": "Action",
        "language": "English",
        "base_price": 12.50
    }
    
    response = requests.post(f"{BASE_URL}/movies/", json=movie_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Movie created successfully")
        return response.json()["id"]
    else:
        print(f"❌ Failed to create movie: {response.text}")
        return None

def test_theater_creation():
    """Test creating a theater"""
    print("\nTesting theater creation...")
    
    theater_data = {
        "name": "Cineplex Downtown",
        "address": "123 Main Street, Downtown",
        "city": "New York",
        "state": "NY",
        "contact_number": "555-0123"
    }
    
    response = requests.post(f"{BASE_URL}/theaters/", json=theater_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Theater created successfully")
        return response.json()["id"]
    else:
        print(f"❌ Failed to create theater: {response.text}")
        return None

def test_hall_creation(theater_id):
    """Test creating a hall"""
    print(f"\nTesting hall creation for theater {theater_id}...")
    
    hall_data = {
        "name": "Hall A",
        "theater_id": theater_id,
        "total_rows": 10
    }
    
    response = requests.post(f"{BASE_URL}/halls/", json=hall_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Hall created successfully")
        return response.json()["id"]
    else:
        print(f"❌ Failed to create hall: {response.text}")
        return None

def test_seat_layout_creation(hall_id):
    """Test creating seat layout"""
    print(f"\nTesting seat layout creation for hall {hall_id}...")
    
    # Create seats with different numbers per row (minimum 6 as required)
    seats_per_row = {
        1: 8,   # Row 1: 8 seats
        2: 7,   # Row 2: 7 seats
        3: 9,   # Row 3: 9 seats
        4: 6,   # Row 4: 6 seats (minimum)
        5: 10,  # Row 5: 10 seats
        6: 8,   # Row 6: 8 seats
        7: 7,   # Row 7: 7 seats
        8: 9,   # Row 8: 9 seats
        9: 6,   # Row 9: 6 seats
        10: 8   # Row 10: 8 seats
    }
    
    response = requests.post(f"{BASE_URL}/seats/layout/{hall_id}", json=seats_per_row)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Seat layout created successfully")
        return True
    else:
        print(f"❌ Failed to create seat layout: {response.text}")
        return False

def test_show_creation(movie_id, hall_id):
    """Test creating a show"""
    print(f"\nTesting show creation for movie {movie_id} in hall {hall_id}...")
    
    show_data = {
        "movie_id": movie_id,
        "hall_id": hall_id,
        "show_date": date.today().isoformat(),
        "start_time": "19:00:00",
        "end_time": "21:23:00",
        "price_multiplier": 1.0,
        "status": "active"
    }
    
    response = requests.post(f"{BASE_URL}/shows/", json=show_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Show created successfully")
        return response.json()["id"]
    else:
        print(f"❌ Failed to create show: {response.text}")
        return None

def test_user_creation():
    """Test creating a user"""
    print("\nTesting user creation...")
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ User created successfully")
        return response.json()["id"]
    else:
        print(f"❌ Failed to create user: {response.text}")
        return None

def test_booking_creation(user_id, show_id):
    """Test creating a booking"""
    print(f"\nTesting booking creation for user {user_id} and show {show_id}...")
    
    # First get available seats
    response = requests.get(f"{BASE_URL}/seats/layout/1")
    if response.status_code == 200:
        layout = response.json()
        available_seats = layout.get("available_seats", [])
        
        if available_seats:
            seat_id = available_seats[0]
            
            booking_data = {
                "show_id": show_id,
                "seat_id": seat_id
            }
            
            response = requests.post(f"{BASE_URL}/bookings/?user_id={user_id}", json=booking_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                print("✅ Booking created successfully")
                return response.json()["id"]
            else:
                print(f"❌ Failed to create booking: {response.text}")
                return None
        else:
            print("❌ No available seats found")
            return None
    else:
        print(f"❌ Failed to get seat layout: {response.text}")
        return None

def main():
    """Run all tests"""
    print("🎬 Movie Booking System API Test")
    print("=" * 40)
    
    # Test basic CRUD operations
    movie_id = test_movie_creation()
    theater_id = test_theater_creation()
    
    if theater_id:
        hall_id = test_hall_creation(theater_id)
        
        if hall_id:
            test_seat_layout_creation(hall_id)
            
            if movie_id:
                show_id = test_show_creation(movie_id, hall_id)
                
                if show_id:
                    user_id = test_user_creation()
                    
                    if user_id:
                        test_booking_creation(user_id, show_id)
    
    print("\n" + "=" * 40)
    print("🏁 Test completed!")
    print(f"📖 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

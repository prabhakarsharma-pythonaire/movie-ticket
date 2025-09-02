#!/usr/bin/env python3
"""
Simple test script to verify the movie booking system functionality
"""

import requests
import json
from datetime import datetime, date

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def test_basic_functionality():
    """Test basic functionality without complex booking features"""
    print("🎬 Testing Basic Movie Booking System Functionality")
    print("=" * 60)
    
    # Test 1: Get all movies
    print("\n1. Testing Movie Retrieval:")
    response = requests.get(f"{BASE_URL}/movies/")
    if response.status_code == 200:
        movies = response.json()
        print(f"✅ Found {len(movies)} movies")
        for movie in movies[:3]:  # Show first 3
            print(f"   - {movie['title']} (${movie['base_price']})")
    else:
        print(f"❌ Failed to get movies: {response.status_code}")
    
    # Test 2: Get all theaters
    print("\n2. Testing Theater Retrieval:")
    response = requests.get(f"{BASE_URL}/theaters/")
    if response.status_code == 200:
        theaters = response.json()
        print(f"✅ Found {len(theaters)} theaters")
        for theater in theaters[:3]:  # Show first 3
            print(f"   - {theater['name']} ({theater['city']})")
    else:
        print(f"❌ Failed to get theaters: {response.status_code}")
    
    # Test 3: Get halls for first theater
    print("\n3. Testing Hall Retrieval:")
    if theaters:
        theater_id = theaters[0]['id']
        response = requests.get(f"{BASE_URL}/halls/theater/{theater_id}")
        if response.status_code == 200:
            halls = response.json()
            print(f"✅ Found {len(halls)} halls for theater {theater_id}")
            for hall in halls:
                print(f"   - {hall['name']} ({hall['total_rows']} rows)")
        else:
            print(f"❌ Failed to get halls: {response.status_code}")
    
    # Test 4: Get seat layout for first hall
    print("\n4. Testing Seat Layout:")
    if halls:
        hall_id = halls[0]['id']
        response = requests.get(f"{BASE_URL}/seats/layout/{hall_id}")
        if response.status_code == 200:
            layout = response.json()
            print(f"✅ Hall layout retrieved:")
            print(f"   - Total rows: {layout['total_rows']}")
            print(f"   - Total seats: {len(layout['available_seats']) + len(layout['booked_seats'])}")
            print(f"   - Available seats: {len(layout['available_seats'])}")
            print(f"   - Booked seats: {len(layout['booked_seats'])}")
        else:
            print(f"❌ Failed to get seat layout: {response.status_code}")
    
    # Test 5: Get shows
    print("\n5. Testing Show Retrieval:")
    response = requests.get(f"{BASE_URL}/shows/")
    if response.status_code == 200:
        shows = response.json()
        print(f"✅ Found {len(shows)} shows")
        for show in shows[:3]:  # Show first 3
            print(f"   - Show {show['id']}: Movie {show['movie_id']}, Hall {show['hall_id']}")
    else:
        print(f"❌ Failed to get shows: {response.status_code}")
    
    # Test 6: Get users
    print("\n6. Testing User Retrieval:")
    response = requests.get(f"{BASE_URL}/users/")
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Found {len(users)} users")
        for user in users[:3]:  # Show first 3
            print(f"   - {user['username']} ({user['email']})")
    else:
        print(f"❌ Failed to get users: {response.status_code}")
    
    # Test 7: Get bookings
    print("\n7. Testing Booking Retrieval:")
    response = requests.get(f"{BASE_URL}/bookings/")
    if response.status_code == 200:
        bookings = response.json()
        print(f"✅ Found {len(bookings)} bookings")
        for booking in bookings[:3]:  # Show first 3
            print(f"   - Booking {booking['id']}: User {booking['user_id']}, Seat {booking['seat_id']}, Ref: {booking['booking_reference']}")
    else:
        print(f"❌ Failed to get bookings: {response.status_code}")
    
    # Test 8: Test single booking (if we have available seats and users)
    print("\n8. Testing Single Booking:")
    if users and shows and layout and layout['available_seats']:
        user_id = users[0]['id']
        show_id = shows[0]['id']
        available_seat = layout['available_seats'][0]
        
        booking_data = {
            "show_id": show_id,
            "seat_id": available_seat
        }
        
        response = requests.post(f"{BASE_URL}/bookings/?user_id={user_id}", json=booking_data)
        if response.status_code == 201:
            booking = response.json()
            print(f"✅ Single booking created successfully:")
            print(f"   - Booking ID: {booking['id']}")
            print(f"   - Reference: {booking['booking_reference']}")
            print(f"   - Amount: ${booking['amount_paid']}")
        else:
            print(f"❌ Failed to create single booking: {response.status_code} - {response.text}")
    else:
        print("⚠️  Skipping single booking test - missing required data")
    
    print("\n" + "=" * 60)
    print("🏁 Basic Functionality Test Complete!")
    print("📖 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    test_basic_functionality()

#!/usr/bin/env python3
"""
Comprehensive test script for the Movie Booking System API
Tests all functionalities from scratch with a fresh database
"""

import requests
import json
import time
from datetime import datetime, date

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"🎬 {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def test_1_movie_creation():
    """Test 1: Movie Creation"""
    print_section("Test 1: Movie Creation")
    
    movies_data = [
        {
            "title": "The Avengers",
            "description": "Earth's mightiest heroes assemble",
            "duration_minutes": 143,
            "genre": "Action",
            "language": "English",
            "base_price": 12.50
        },
        {
            "title": "Inception",
            "description": "A thief who steals corporate secrets through dream-sharing technology",
            "duration_minutes": 148,
            "genre": "Sci-Fi",
            "language": "English",
            "base_price": 15.00
        },
        {
            "title": "The Dark Knight",
            "description": "Batman faces his greatest challenge",
            "duration_minutes": 152,
            "genre": "Action",
            "language": "English",
            "base_price": 14.50
        }
    ]
    
    created_movies = []
    for i, movie_data in enumerate(movies_data):
        response = requests.post(f"{BASE_URL}/movies/", json=movie_data)
        if response.status_code == 201:
            movie = response.json()
            created_movies.append(movie)
            print_success(f"Created movie {i+1}: {movie['title']} (ID: {movie['id']})")
        else:
            print_error(f"Failed to create movie {i+1}: {response.text}")
    
    return created_movies

def test_2_theater_creation():
    """Test 2: Theater Creation"""
    print_section("Test 2: Theater Creation")
    
    theaters_data = [
        {
            "name": "Cineplex Downtown",
            "address": "123 Main Street, Downtown",
            "city": "New York",
            "state": "NY",
            "contact_number": "555-0123"
        },
        {
            "name": "Multiplex Central",
            "address": "456 Entertainment Ave, Downtown",
            "city": "Mumbai",
            "state": "Maharashtra",
            "contact_number": "555-0456"
        }
    ]
    
    created_theaters = []
    for i, theater_data in enumerate(theaters_data):
        response = requests.post(f"{BASE_URL}/theaters/", json=theater_data)
        if response.status_code == 201:
            theater = response.json()
            created_theaters.append(theater)
            print_success(f"Created theater {i+1}: {theater['name']} (ID: {theater['id']})")
        else:
            print_error(f"Failed to create theater {i+1}: {response.text}")
    
    return created_theaters

def test_3_hall_creation(theaters):
    """Test 3: Hall Creation"""
    print_section("Test 3: Hall Creation")
    
    halls_data = [
        {
            "name": "Hall A",
            "theater_id": theaters[0]['id'],
            "total_rows": 8
        },
        {
            "name": "Hall B",
            "theater_id": theaters[0]['id'],
            "total_rows": 6
        },
        {
            "name": "Premium Hall",
            "theater_id": theaters[1]['id'],
            "total_rows": 10
        }
    ]
    
    created_halls = []
    for i, hall_data in enumerate(halls_data):
        response = requests.post(f"{BASE_URL}/halls/", json=hall_data)
        if response.status_code == 201:
            hall = response.json()
            created_halls.append(hall)
            print_success(f"Created hall {i+1}: {hall['name']} (ID: {hall['id']})")
        else:
            print_error(f"Failed to create hall {i+1}: {response.text}")
    
    return created_halls

def test_4_seat_layout_creation(halls):
    """Test 4: Seat Layout Creation"""
    print_section("Test 4: Seat Layout Creation")
    
    # Create different seat layouts for each hall
    seat_layouts = [
        # Hall A: 8 rows with different seats per row
        {
            1: 10,  # Row 1: 10 seats
            2: 8,   # Row 2: 8 seats
            3: 12,  # Row 3: 12 seats
            4: 6,   # Row 4: 6 seats (minimum)
            5: 9,   # Row 5: 9 seats
            6: 7,   # Row 6: 7 seats
            7: 11,  # Row 7: 11 seats
            8: 8    # Row 8: 8 seats
        },
        # Hall B: 6 rows with different seats per row
        {
            1: 8,   # Row 1: 8 seats
            2: 6,   # Row 2: 6 seats (minimum)
            3: 10,  # Row 3: 10 seats
            4: 7,   # Row 4: 7 seats
            5: 9,   # Row 5: 9 seats
            6: 8    # Row 6: 8 seats
        },
        # Premium Hall: 10 rows with different seats per row
        {
            1: 12,  # Row 1: 12 seats
            2: 10,  # Row 2: 10 seats
            3: 14,  # Row 3: 14 seats
            4: 8,   # Row 4: 8 seats
            5: 11,  # Row 5: 11 seats
            6: 9,   # Row 6: 9 seats
            7: 13,  # Row 7: 13 seats
            8: 10,  # Row 8: 10 seats
            9: 12,  # Row 9: 12 seats
            10: 8   # Row 10: 8 seats
        }
    ]
    
    created_layouts = []
    for i, hall in enumerate(halls):
        response = requests.post(f"{BASE_URL}/seats/layout/{hall['id']}", json=seat_layouts[i])
        if response.status_code == 201:
            seats = response.json()
            created_layouts.append(seats)
            print_success(f"Created seat layout for {hall['name']}: {len(seats)} seats")
        else:
            print_error(f"Failed to create seat layout for {hall['name']}: {response.text}")
    
    return created_layouts

def test_5_show_creation(movies, halls):
    """Test 5: Show Creation"""
    print_section("Test 5: Show Creation")
    
    shows_data = [
        {
            "movie_id": movies[0]['id'],  # The Avengers
            "hall_id": halls[0]['id'],    # Hall A
            "show_date": date.today().isoformat(),
            "start_time": "14:00:00",
            "end_time": "16:23:00",
            "price_multiplier": 1.0,
            "status": "active"
        },
        {
            "movie_id": movies[0]['id'],  # The Avengers
            "hall_id": halls[0]['id'],    # Hall A
            "show_date": date.today().isoformat(),
            "start_time": "18:00:00",
            "end_time": "20:23:00",
            "price_multiplier": 1.2,  # Premium pricing
            "status": "active"
        },
        {
            "movie_id": movies[1]['id'],  # Inception
            "hall_id": halls[1]['id'],    # Hall B
            "show_date": date.today().isoformat(),
            "start_time": "19:00:00",
            "end_time": "21:28:00",
            "price_multiplier": 1.0,
            "status": "active"
        },
        {
            "movie_id": movies[2]['id'],  # The Dark Knight
            "hall_id": halls[2]['id'],    # Premium Hall
            "show_date": date.today().isoformat(),
            "start_time": "20:00:00",
            "end_time": "22:32:00",
            "price_multiplier": 1.5,  # Premium pricing
            "status": "active"
        }
    ]
    
    created_shows = []
    for i, show_data in enumerate(shows_data):
        response = requests.post(f"{BASE_URL}/shows/", json=show_data)
        if response.status_code == 201:
            show = response.json()
            created_shows.append(show)
            print_success(f"Created show {i+1}: {show['start_time']} (ID: {show['id']})")
        else:
            print_error(f"Failed to create show {i+1}: {response.text}")
    
    return created_shows

def test_6_user_creation():
    """Test 6: User Creation"""
    print_section("Test 6: User Creation")
    
    users_data = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "password123"
        },
        {
            "username": "alice_smith",
            "email": "alice@example.com",
            "full_name": "Alice Smith",
            "password": "securepass456"
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "full_name": "Bob Wilson",
            "password": "mypassword789"
        }
    ]
    
    created_users = []
    for i, user_data in enumerate(users_data):
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 201:
            user = response.json()
            created_users.append(user)
            print_success(f"Created user {i+1}: {user['username']} (ID: {user['id']})")
        else:
            print_error(f"Failed to create user {i+1}: {response.text}")
    
    return created_users

def test_7_single_bookings(users, shows):
    """Test 7: Single Bookings"""
    print_section("Test 7: Single Bookings")
    
    created_bookings = []
    
    # Create single bookings for different users and shows
    for i, user in enumerate(users):
        if i < len(shows):
            show = shows[i]
            
            # Get the hall for this show
            hall_id = show['hall_id']
            response = requests.get(f"{BASE_URL}/seats/layout/{hall_id}")
            
            if response.status_code == 200:
                layout = response.json()
                
                if layout['available_seats']:
                    seat_id = layout['available_seats'][0]
                    
                    booking_data = {
                        "show_id": show['id'],
                        "seat_id": seat_id
                    }
                    
                    response = requests.post(f"{BASE_URL}/bookings/?user_id={user['id']}", json=booking_data)
                    if response.status_code == 201:
                        booking = response.json()
                        created_bookings.append(booking)
                        print_success(f"Created booking for {user['username']}: Seat {seat_id} (ID: {booking['id']})")
                    else:
                        print_error(f"Failed to create booking for {user['username']}: {response.text}")
                else:
                    print_info(f"No available seats for {user['username']} in show {show['id']}")
            else:
                print_error(f"Failed to get seat layout for hall {hall_id}")
    
    return created_bookings

def test_8_group_bookings(users, shows):
    """Test 8: Group Bookings"""
    print_section("Test 8: Group Bookings")
    
    created_group_bookings = []
    
    # Try group booking for each show
    for i, show in enumerate(shows):
        user = users[i % len(users)]
        
        # Get the hall for this show
        hall_id = show['hall_id']
        response = requests.get(f"{BASE_URL}/seats/layout/{hall_id}")
        
        if response.status_code == 200:
            layout = response.json()
            
            # Find 3 consecutive available seats
            available_seats = layout['available_seats']
            if len(available_seats) >= 3:
                seat_ids = available_seats[:3]  # Take first 3 available seats
                
                group_booking_data = {
                    "show_id": show['id'],
                    "seat_ids": seat_ids,
                    "user_id": user['id']
                }
                
                response = requests.post(f"{BASE_URL}/bookings/group", json=group_booking_data)
                if response.status_code == 201:
                    bookings = response.json()
                    created_group_bookings.extend(bookings)
                    print_success(f"Created group booking for {user['username']}: {len(bookings)} seats")
                else:
                    print_error(f"Failed to create group booking for {user['username']}: {response.text}")
            else:
                print_info(f"Not enough available seats for group booking in show {show['id']}")
        else:
            print_error(f"Failed to get seat layout for hall {hall_id}")
    
    return created_group_bookings

def test_9_consecutive_bookings(users, shows):
    """Test 9: Consecutive Seat Bookings"""
    print_section("Test 9: Consecutive Seat Bookings")
    
    created_consecutive_bookings = []
    
    # Try consecutive booking for each show
    for i, show in enumerate(shows):
        user = users[i % len(users)]
        
        response = requests.post(f"{BASE_URL}/bookings/group/consecutive?show_id={show['id']}&num_seats=3&user_id={user['id']}")
        if response.status_code == 201:
            bookings = response.json()
            created_consecutive_bookings.extend(bookings)
            print_success(f"Created consecutive booking for {user['username']}: {len(bookings)} seats")
        else:
            print_error(f"Failed to create consecutive booking for {user['username']}: {response.text}")
    
    return created_consecutive_bookings

def test_10_alternative_suggestions(movies):
    """Test 10: Alternative Booking Suggestions"""
    print_section("Test 10: Alternative Booking Suggestions")
    
    for movie in movies:
        response = requests.get(f"{BASE_URL}/bookings/alternatives/{movie['id']}?num_seats=4")
        if response.status_code == 200:
            alternatives = response.json()
            if alternatives:
                print_success(f"Found {len(alternatives)} alternatives for {movie['title']}")
                for alt in alternatives[:2]:  # Show first 2
                    print_info(f"  - {alt['theater_name']}: {alt['start_time']} ({alt['total_available']} seats)")
            else:
                print_info(f"No alternatives found for {movie['title']}")
        else:
            print_error(f"Failed to get alternatives for {movie['title']}: {response.text}")

def test_11_booking_management(users):
    """Test 11: Booking Management"""
    print_section("Test 11: Booking Management")
    
    for user in users:
        # Get user's bookings
        response = requests.get(f"{BASE_URL}/bookings/user/{user['id']}")
        if response.status_code == 200:
            bookings = response.json()
            print_success(f"User {user['username']} has {len(bookings)} bookings")
            
            # Cancel the first booking if available
            if bookings:
                booking_id = bookings[0]['id']
                cancel_response = requests.put(f"{BASE_URL}/bookings/{booking_id}/cancel")
                if cancel_response.status_code == 200:
                    print_success(f"Cancelled booking {booking_id} for {user['username']}")
                else:
                    print_error(f"Failed to cancel booking {booking_id}: {cancel_response.text}")
        else:
            print_error(f"Failed to get bookings for {user['username']}: {response.text}")

def test_12_data_retrieval():
    """Test 12: Data Retrieval and Validation"""
    print_section("Test 12: Data Retrieval and Validation")
    
    # Get all data and validate
    endpoints = [
        ("movies", "Movies"),
        ("theaters", "Theaters"),
        ("halls", "Halls"),
        ("shows", "Shows"),
        ("users", "Users"),
        ("bookings", "Bookings")
    ]
    
    for endpoint, name in endpoints:
        response = requests.get(f"{BASE_URL}/{endpoint}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data)} {name}")
        else:
            print_error(f"Failed to retrieve {name}: {response.status_code}")

def main():
    """Run all tests"""
    print("🎬 Movie Booking System - Comprehensive Test Suite")
    print("=" * 80)
    print("Testing all functionalities from scratch with fresh database")
    print("=" * 80)
    
    try:
        # Test 1-6: Create all entities
        movies = test_1_movie_creation()
        theaters = test_2_theater_creation()
        halls = test_3_hall_creation(theaters)
        layouts = test_4_seat_layout_creation(halls)
        shows = test_5_show_creation(movies, halls)
        users = test_6_user_creation()
        
        # Test 7-9: Test booking functionality
        single_bookings = test_7_single_bookings(users, shows)
        group_bookings = test_8_group_bookings(users, shows)
        consecutive_bookings = test_9_consecutive_bookings(users, shows)
        
        # Test 10-12: Test advanced features
        test_10_alternative_suggestions(movies)
        test_11_booking_management(users)
        test_12_data_retrieval()
        
        # Summary
        print_section("Test Summary")
        print_success("All tests completed!")
        print_info(f"Created: {len(movies)} movies, {len(theaters)} theaters, {len(halls)} halls")
        print_info(f"Created: {len(shows)} shows, {len(users)} users")
        print_info(f"Created: {len(single_bookings)} single bookings, {len(group_bookings)} group bookings")
        print_info(f"Created: {len(consecutive_bookings)} consecutive bookings")
        
        print(f"\n📖 API Documentation: http://localhost:8000/docs")
        print(f"🔗 API Base URL: http://localhost:8000/api/v1")
        
    except Exception as e:
        print_error(f"Test suite failed with error: {str(e)}")

if __name__ == "__main__":
    main()

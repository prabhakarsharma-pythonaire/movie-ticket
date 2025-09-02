#!/usr/bin/env python3
"""
Simple Analytics Test to verify functionality
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000/api/v1"

def test_analytics():
    print("🧪 Testing Analytics with Current Data")
    print("=" * 50)
    
    # Test 1: Get all bookings
    print("\n1. Current Booking Data:")
    response = requests.get(f"{BASE_URL}/bookings/")
    if response.status_code == 200:
        bookings = response.json()
        confirmed_bookings = [b for b in bookings if b['status'] == 'confirmed']
        total_revenue = sum(b['amount_paid'] for b in confirmed_bookings)
        
        print(f"   Total Bookings: {len(bookings)}")
        print(f"   Confirmed Bookings: {len(confirmed_bookings)}")
        print(f"   Total Revenue: ${total_revenue}")
        print(f"   Average Booking Value: ${total_revenue/len(confirmed_bookings) if confirmed_bookings else 0:.2f}")
    
    # Test 2: Get shows
    print("\n2. Current Show Data:")
    response = requests.get(f"{BASE_URL}/shows/")
    if response.status_code == 200:
        shows = response.json()
        print(f"   Total Shows: {len(shows)}")
        for show in shows:
            print(f"   - Show {show['id']}: Movie {show['movie_id']}, Date: {show['show_date']}")
    
    # Test 3: Test analytics with default date range
    print("\n3. Analytics with Default Date Range:")
    response = requests.get(f"{BASE_URL}/analytics/revenue")
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Total Revenue: ${data['total_revenue']}")
        print(f"   Total Bookings: {data['total_bookings']}")
        print(f"   Period: {data['period_start']} to {data['period_end']}")
    
    # Test 4: Test analytics with specific date range
    print("\n4. Analytics with Specific Date Range (2025-08-30 to 2025-08-31):")
    response = requests.get(f"{BASE_URL}/analytics/revenue?start_date=2025-08-30&end_date=2025-08-31")
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Total Revenue: ${data['total_revenue']}")
        print(f"   Total Bookings: {data['total_bookings']}")
        print(f"   Period: {data['period_start']} to {data['period_end']}")
    
    # Test 5: Test top movies
    print("\n5. Top Movies Analytics:")
    response = requests.get(f"{BASE_URL}/analytics/top-movies?limit=3")
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Found {len(data)} top movies")
        for movie in data:
            print(f"   - {movie['movie_title']}: ${movie['total_revenue']}")
    
    # Test 6: Test seat utilization
    print("\n6. Seat Utilization Analytics:")
    response = requests.get(f"{BASE_URL}/analytics/seat-utilization")
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Overall Utilization: {data['overall_utilization']}%")
        print(f"   Total Shows: {data['total_shows']}")
        print(f"   Total Seats Available: {data['total_seats_available']}")
        print(f"   Total Seats Booked: {data['total_seats_booked']}")

if __name__ == "__main__":
    test_analytics()

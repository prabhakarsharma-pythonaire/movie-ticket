#!/usr/bin/env python3
"""
Simple Analytics Test Script
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000/api/v1"

def test_analytics():
    print("🧪 Testing Analytics Endpoints")
    print("=" * 50)
    
    # Test 1: Revenue Analytics with booking date filter
    print("\n1. Testing Revenue Analytics:")
    response = requests.get(f"{BASE_URL}/analytics/revenue")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total Revenue: ${data['total_revenue']}")
        print(f"Total Bookings: {data['total_bookings']}")
        print(f"Period: {data['period_start']} to {data['period_end']}")
    
    # Test 2: Top Movies
    print("\n2. Testing Top Movies:")
    response = requests.get(f"{BASE_URL}/analytics/top-movies?limit=3")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} top movies")
        for movie in data:
            print(f"  - {movie['movie_title']}: ${movie['total_revenue']}")
    
    # Test 3: Top Theaters
    print("\n3. Testing Top Theaters:")
    response = requests.get(f"{BASE_URL}/analytics/top-theaters?limit=3")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} top theaters")
        for theater in data:
            print(f"  - {theater['theater_name']}: ${theater['total_revenue']}")
    
    # Test 4: Seat Utilization
    print("\n4. Testing Seat Utilization:")
    response = requests.get(f"{BASE_URL}/analytics/seat-utilization")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Overall Utilization: {data['overall_utilization']}%")
        print(f"Total Shows: {data['total_shows']}")
        print(f"Total Seats Available: {data['total_seats_available']}")
        print(f"Total Seats Booked: {data['total_seats_booked']}")

if __name__ == "__main__":
    test_analytics()

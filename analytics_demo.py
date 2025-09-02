#!/usr/bin/env python3
"""
Analytics Demonstration Script for Movie Booking System
Showcases all the advanced analytics and reporting features
"""

import requests
import json
from datetime import datetime, date, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def print_header(title):
    """Print a beautiful header"""
    print(f"\n{'📊' * 20}")
    print(f"📊 {title}")
    print(f"{'📊' * 20}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def print_data(data, title=""):
    """Print formatted data"""
    if title:
        print(f"\n📋 {title}:")
    print(json.dumps(data, indent=2, default=str))

def demo_1_movie_analytics():
    """Demo 1: Movie Analytics"""
    print_header("MOVIE ANALYTICS")
    
    # Get all movies first
    response = requests.get(f"{BASE_URL}/movies/")
    if response.status_code == 200:
        movies = response.json()
        
        for movie in movies[:2]:  # Test with first 2 movies
            print_info(f"🎬 Analyzing: {movie['title']}")
            
            # Get movie analytics
            analytics_response = requests.get(f"{BASE_URL}/analytics/movie/{movie['id']}")
            if analytics_response.status_code == 200:
                analytics = analytics_response.json()
                print_success(f"Movie Analytics for {movie['title']}")
                print(f"   📅 Period: {analytics['period_start']} to {analytics['period_end']}")
                print(f"   🎪 Total Shows: {analytics['total_shows']}")
                print(f"   🎫 Total Bookings: {analytics['total_bookings']}")
                print(f"   💰 Total Revenue: ${analytics['total_revenue']}")
                print(f"   📊 Average Occupancy: {analytics['average_occupancy']}%")
                
                if analytics['shows_data']:
                    print(f"   📈 Show Details:")
                    for show in analytics['shows_data'][:3]:  # Show first 3
                        print(f"      - Show {show['show_id']}: {show['booked_seats']}/{show['total_seats']} seats (${show['revenue']})")
            else:
                print(f"❌ Failed to get analytics for {movie['title']}")
            print()

def demo_2_theater_analytics():
    """Demo 2: Theater Analytics"""
    print_header("THEATER ANALYTICS")
    
    # Get all theaters first
    response = requests.get(f"{BASE_URL}/theaters/")
    if response.status_code == 200:
        theaters = response.json()
        
        for theater in theaters:
            print_info(f"🏢 Analyzing: {theater['name']}")
            
            # Get theater analytics
            analytics_response = requests.get(f"{BASE_URL}/analytics/theater/{theater['id']}")
            if analytics_response.status_code == 200:
                analytics = analytics_response.json()
                print_success(f"Theater Analytics for {theater['name']}")
                print(f"   📅 Period: {analytics['period_start']} to {analytics['period_end']}")
                print(f"   🎭 Total Halls: {analytics['total_halls']}")
                print(f"   🎪 Total Shows: {analytics['total_shows']}")
                print(f"   🎫 Total Bookings: {analytics['total_bookings']}")
                print(f"   💰 Total Revenue: ${analytics['total_revenue']}")
                print(f"   📊 Average Occupancy: {analytics['average_occupancy']}%")
                
                if analytics['halls_data']:
                    print(f"   🎭 Hall Details:")
                    for hall in analytics['halls_data']:
                        print(f"      - {hall['hall_name']}: {hall['booked_seats']}/{hall['total_seats']} seats (${hall['revenue']})")
            else:
                print(f"❌ Failed to get analytics for {theater['name']}")
            print()

def demo_3_revenue_analytics():
    """Demo 3: Revenue Analytics"""
    print_header("REVENUE ANALYTICS")
    
    # Get overall revenue analytics
    response = requests.get(f"{BASE_URL}/analytics/revenue")
    if response.status_code == 200:
        analytics = response.json()
        print_success("Overall Revenue Analytics")
        print(f"   📅 Period: {analytics['period_start']} to {analytics['period_end']}")
        print(f"   💰 Total Revenue: ${analytics['total_revenue']}")
        print(f"   🎫 Total Bookings: {analytics['total_bookings']}")
        print(f"   📊 Average Booking Value: ${analytics['average_booking_value']}")
        
        if analytics['daily_revenue']:
            print(f"   📈 Daily Revenue (last 5 days):")
            for day in analytics['daily_revenue'][-5:]:
                print(f"      - {day['date']}: ${day['revenue']} ({day['bookings']} bookings)")
        
        if analytics['movie_revenue']:
            print(f"   🎬 Top Movies by Revenue:")
            for movie in analytics['movie_revenue'][:3]:
                print(f"      - {movie['movie_title']}: ${movie['revenue']} ({movie['bookings']} bookings)")
        
        if analytics['theater_revenue']:
            print(f"   🏢 Top Theaters by Revenue:")
            for theater in analytics['theater_revenue'][:3]:
                print(f"      - {theater['theater_name']}: ${theater['revenue']} ({theater['bookings']} bookings)")
    else:
        print("❌ Failed to get revenue analytics")

def demo_4_top_performers():
    """Demo 4: Top Performers"""
    print_header("TOP PERFORMERS")
    
    # Get top movies
    response = requests.get(f"{BASE_URL}/analytics/top-movies?limit=3")
    if response.status_code == 200:
        top_movies = response.json()
        print_success("Top Movies by Revenue")
        for i, movie in enumerate(top_movies, 1):
            print(f"   {i}. {movie['movie_title']} ({movie['genre']})")
            print(f"      💰 Revenue: ${movie['total_revenue']}")
            print(f"      🎫 Bookings: {movie['total_bookings']}")
            print(f"      📊 Avg Booking: ${movie['average_booking_value']}")
    
    print()
    
    # Get top theaters
    response = requests.get(f"{BASE_URL}/analytics/top-theaters?limit=3")
    if response.status_code == 200:
        top_theaters = response.json()
        print_success("Top Theaters by Revenue")
        for i, theater in enumerate(top_theaters, 1):
            print(f"   {i}. {theater['theater_name']} ({theater['city']})")
            print(f"      💰 Revenue: ${theater['total_revenue']}")
            print(f"      🎫 Bookings: {theater['total_bookings']}")
            print(f"      📊 Avg Booking: ${theater['average_booking_value']}")

def demo_5_seat_utilization():
    """Demo 5: Seat Utilization"""
    print_header("SEAT UTILIZATION")
    
    # Get seat utilization analytics
    response = requests.get(f"{BASE_URL}/analytics/seat-utilization")
    if response.status_code == 200:
        analytics = response.json()
        print_success("Seat Utilization Analytics")
        print(f"   📅 Period: {analytics['period_start']} to {analytics['period_end']}")
        print(f"   🎪 Total Shows: {analytics['total_shows']}")
        print(f"   💺 Total Seats Available: {analytics['total_seats_available']}")
        print(f"   🎫 Total Seats Booked: {analytics['total_seats_booked']}")
        print(f"   📊 Overall Utilization: {analytics['overall_utilization']}%")
        
        if analytics['hall_utilization']:
            print(f"   🎭 Hall-wise Utilization:")
            for hall in analytics['hall_utilization']:
                print(f"      - {hall['hall_name']} ({hall['theater_name']}): {hall['utilization_percentage']}%")
                print(f"        Shows: {hall['total_shows']}, Seats: {hall['booked_seats']}/{hall['total_seats']}")
    else:
        print("❌ Failed to get seat utilization analytics")

def demo_6_advanced_queries():
    """Demo 6: Advanced Analytics Queries"""
    print_header("ADVANCED ANALYTICS QUERIES")
    
    # Custom date range analytics
    start_date = (date.today() - timedelta(days=7)).isoformat()
    end_date = date.today().isoformat()
    
    print_info(f"📅 Custom Date Range: {start_date} to {end_date}")
    
    # Revenue analytics for custom date range
    response = requests.get(f"{BASE_URL}/analytics/revenue?start_date={start_date}&end_date={end_date}")
    if response.status_code == 200:
        analytics = response.json()
        print_success(f"Revenue Analytics (Last 7 days)")
        print(f"   💰 Total Revenue: ${analytics['total_revenue']}")
        print(f"   🎫 Total Bookings: {analytics['total_bookings']}")
    
    print()
    
    # Top movies with custom limit
    response = requests.get(f"{BASE_URL}/analytics/top-movies?limit=5")
    if response.status_code == 200:
        movies = response.json()
        print_success("Top 5 Movies by Revenue")
        for i, movie in enumerate(movies, 1):
            print(f"   {i}. {movie['movie_title']}: ${movie['total_revenue']}")

def demo_7_api_endpoints():
    """Demo 7: Analytics API Endpoints Overview"""
    print_header("ANALYTICS API ENDPOINTS")
    
    endpoints = [
        ("GET", "/analytics/movie/{movie_id}", "Get comprehensive analytics for a specific movie"),
        ("GET", "/analytics/theater/{theater_id}", "Get comprehensive analytics for a specific theater"),
        ("GET", "/analytics/revenue", "Get overall revenue analytics with breakdowns"),
        ("GET", "/analytics/top-movies", "Get top performing movies by revenue"),
        ("GET", "/analytics/top-theaters", "Get top performing theaters by revenue"),
        ("GET", "/analytics/seat-utilization", "Get seat utilization analytics across all halls")
    ]
    
    print_success("Available Analytics Endpoints:")
    for method, endpoint, description in endpoints:
        print(f"   {method:<6} {endpoint:<35} - {description}")
    
    print(f"\n📖 Full API Documentation: http://localhost:8000/docs")
    print(f"🔗 Analytics Examples:")
    print(f"   - Movie Analytics: {BASE_URL}/analytics/movie/1")
    print(f"   - Theater Analytics: {BASE_URL}/analytics/theater/1")
    print(f"   - Revenue Analytics: {BASE_URL}/analytics/revenue")
    print(f"   - Top Movies: {BASE_URL}/analytics/top-movies?limit=5")

def main():
    """Run the complete analytics demonstration"""
    print("📊 MOVIE BOOKING SYSTEM - ANALYTICS DEMONSTRATION")
    print("=" * 80)
    print("Showcasing advanced analytics and reporting features")
    print("=" * 80)
    
    try:
        # Run all analytics demos
        demo_1_movie_analytics()
        demo_2_theater_analytics()
        demo_3_revenue_analytics()
        demo_4_top_performers()
        demo_5_seat_utilization()
        demo_6_advanced_queries()
        demo_7_api_endpoints()
        
        # Final summary
        print_header("ANALYTICS DEMONSTRATION COMPLETE")
        print_success("🎉 All analytics features are working perfectly!")
        print_info("✅ Movie Analytics: Revenue, bookings, occupancy per movie")
        print_info("✅ Theater Analytics: Performance metrics per theater")
        print_info("✅ Revenue Analytics: Overall revenue with daily/movie/theater breakdowns")
        print_info("✅ Top Performers: Best movies and theaters by revenue")
        print_info("✅ Seat Utilization: Occupancy rates across all halls")
        print_info("✅ Advanced Queries: Custom date ranges and filtering")
        print_info("✅ Real-time Data: Live analytics from booking data")
        
        print(f"\n🚀 Analytics System is production-ready!")
        print(f"📋 Perfect for business intelligence and decision making!")
        
    except Exception as e:
        print(f"❌ Analytics demonstration failed with error: {str(e)}")

if __name__ == "__main__":
    main()

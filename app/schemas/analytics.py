from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class ShowAnalyticsData(BaseModel):
    show_id: int
    show_date: date
    start_time: str
    total_seats: int
    booked_seats: int
    revenue: float
    occupancy_percentage: float

class MovieAnalyticsResponse(BaseModel):
    movie_id: int
    movie_title: str
    period_start: date
    period_end: date
    total_shows: int
    total_bookings: int
    total_revenue: float
    total_tickets: int
    average_occupancy: float
    shows_data: List[ShowAnalyticsData]

class HallAnalyticsData(BaseModel):
    hall_id: int
    hall_name: str
    total_shows: int
    total_seats: int
    booked_seats: int
    revenue: float
    occupancy_percentage: float

class TheaterAnalyticsResponse(BaseModel):
    theater_id: int
    theater_name: str
    period_start: date
    period_end: date
    total_halls: int
    total_shows: int
    total_bookings: int
    total_revenue: float
    average_occupancy: float
    halls_data: List[HallAnalyticsData]

class DailyRevenueData(BaseModel):
    date: str
    revenue: float
    bookings: int

class MovieRevenueData(BaseModel):
    movie_title: str
    revenue: float
    bookings: int

class TheaterRevenueData(BaseModel):
    theater_name: str
    revenue: float
    bookings: int

class RevenueAnalyticsResponse(BaseModel):
    period_start: date
    period_end: date
    total_revenue: float
    total_bookings: int
    average_booking_value: float
    daily_revenue: List[DailyRevenueData]
    movie_revenue: List[MovieRevenueData]
    theater_revenue: List[TheaterRevenueData]

class TopMoviesResponse(BaseModel):
    movie_id: int
    movie_title: str
    genre: str
    total_revenue: float
    total_bookings: int
    average_booking_value: float

class TopTheatersResponse(BaseModel):
    theater_id: int
    theater_name: str
    city: str
    total_revenue: float
    total_bookings: int
    average_booking_value: float

class HallUtilizationData(BaseModel):
    hall_id: int
    hall_name: str
    theater_name: str
    total_shows: int
    total_seats: int
    booked_seats: int
    utilization_percentage: float

class SeatUtilizationResponse(BaseModel):
    period_start: date
    period_end: date
    total_shows: int
    total_seats_available: int
    total_seats_booked: int
    overall_utilization: float
    hall_utilization: List[HallUtilizationData]

class UserAnalyticsResponse(BaseModel):
    total_users: int
    active_users: int
    total_bookings: int
    average_bookings_per_user: float
    top_users: List[dict]

class BookingAnalyticsResponse(BaseModel):
    total_bookings: int
    confirmed_bookings: int
    cancelled_bookings: int
    total_revenue: float
    average_booking_value: float
    booking_trends: List[dict]

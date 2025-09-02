from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, extract
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.core.database import get_db
from app.models.booking import Booking
from app.models.movie import Movie
from app.models.show import Show
from app.models.theater import Theater, Hall
from app.models.user import User
from app.schemas.analytics import (
    MovieAnalyticsResponse,
    TheaterAnalyticsResponse,
    RevenueAnalyticsResponse,
    TopMoviesResponse,
    TopTheatersResponse,
    SeatUtilizationResponse
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/movie/{movie_id}", response_model=MovieAnalyticsResponse)
def get_movie_analytics(
    movie_id: int,
    start_date: Optional[date] = Query(None, description="Start date for analytics (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for analytics (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for a specific movie."""
    
    # Validate movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Set default date range if not provided (last 30 days)
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get all shows for this movie in the date range
    shows = db.query(Show).filter(
        and_(
            Show.movie_id == movie_id,
            Show.show_date >= start_date,
            Show.show_date <= end_date
        )
    ).all()
    
    show_ids = [show.id for show in shows]
    
    if not show_ids:
        return MovieAnalyticsResponse(
            movie_id=movie_id,
            movie_title=movie.title,
            period_start=start_date,
            period_end=end_date,
            total_shows=0,
            total_bookings=0,
            total_revenue=0.0,
            total_tickets=0,
            average_occupancy=0.0,
            shows_data=[]
        )
    
    # Get booking statistics
    booking_stats = db.query(
        func.count(Booking.id).label('total_bookings'),
        func.sum(Booking.amount_paid).label('total_revenue'),
        func.count(Booking.id).label('total_tickets')
    ).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).first()
    
    # Calculate total seats available
    total_seats_available = 0
    shows_data = []
    
    for show in shows:
        # Get hall for this show
        hall = db.query(Hall).filter(Hall.id == show.hall_id).first()
        if hall:
            # Get total seats in this hall
            total_seats = db.query(func.count(Booking.id)).filter(
                Booking.show_id == show.id
            ).scalar() or 0
            
            # Get booked seats for this show
            booked_seats = db.query(func.count(Booking.id)).filter(
                and_(
                    Booking.show_id == show.id,
                    Booking.status == "confirmed"
                )
            ).scalar() or 0
            
            # Get revenue for this show
            show_revenue = db.query(func.sum(Booking.amount_paid)).filter(
                and_(
                    Booking.show_id == show.id,
                    Booking.status == "confirmed"
                )
            ).scalar() or 0.0
            
            # Calculate occupancy
            occupancy = (booked_seats / total_seats * 100) if total_seats > 0 else 0
            
            shows_data.append({
                "show_id": show.id,
                "show_date": show.show_date,
                "start_time": show.start_time,
                "total_seats": total_seats,
                "booked_seats": booked_seats,
                "revenue": float(show_revenue),
                "occupancy_percentage": round(occupancy, 2)
            })
            
            total_seats_available += total_seats
    
    # Calculate average occupancy
    total_booked = booking_stats.total_bookings or 0
    average_occupancy = (total_booked / total_seats_available * 100) if total_seats_available > 0 else 0
    
    return MovieAnalyticsResponse(
        movie_id=movie_id,
        movie_title=movie.title,
        period_start=start_date,
        period_end=end_date,
        total_shows=len(shows),
        total_bookings=total_booked,
        total_revenue=float(booking_stats.total_revenue or 0),
        total_tickets=total_booked,
        average_occupancy=round(average_occupancy, 2),
        shows_data=shows_data
    )

@router.get("/theater/{theater_id}", response_model=TheaterAnalyticsResponse)
def get_theater_analytics(
    theater_id: int,
    start_date: Optional[date] = Query(None, description="Start date for analytics (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for analytics (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for a specific theater."""
    
    # Validate theater exists
    theater = db.query(Theater).filter(Theater.id == theater_id).first()
    if not theater:
        raise HTTPException(status_code=404, detail="Theater not found")
    
    # Set default date range if not provided (last 30 days)
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get all halls for this theater
    halls = db.query(Hall).filter(Hall.theater_id == theater_id).all()
    hall_ids = [hall.id for hall in halls]
    
    if not hall_ids:
        return TheaterAnalyticsResponse(
            theater_id=theater_id,
            theater_name=theater.name,
            period_start=start_date,
            period_end=end_date,
            total_halls=0,
            total_shows=0,
            total_bookings=0,
            total_revenue=0.0,
            average_occupancy=0.0,
            halls_data=[]
        )
    
    # Get all shows for this theater's halls in the date range
    shows = db.query(Show).filter(
        and_(
            Show.hall_id.in_(hall_ids),
            Show.show_date >= start_date,
            Show.show_date <= end_date
        )
    ).all()
    
    show_ids = [show.id for show in shows]
    
    if not show_ids:
        return TheaterAnalyticsResponse(
            theater_id=theater_id,
            theater_name=theater.name,
            period_start=start_date,
            period_end=end_date,
            total_halls=len(halls),
            total_shows=0,
            total_bookings=0,
            total_revenue=0.0,
            average_occupancy=0.0,
            halls_data=[]
        )
    
    # Get booking statistics
    booking_stats = db.query(
        func.count(Booking.id).label('total_bookings'),
        func.sum(Booking.amount_paid).label('total_revenue')
    ).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).first()
    
    # Calculate hall-wise analytics
    halls_data = []
    total_seats_available = 0
    total_booked_seats = 0
    
    for hall in halls:
        # Get shows for this hall
        hall_shows = [show for show in shows if show.hall_id == hall.id]
        hall_show_ids = [show.id for show in hall_shows]
        
        if hall_show_ids:
            # Get total seats in this hall
            total_seats = db.query(func.count(Booking.id)).filter(
                Booking.show_id.in_(hall_show_ids)
            ).scalar() or 0
            
            # Get booked seats for this hall
            booked_seats = db.query(func.count(Booking.id)).filter(
                and_(
                    Booking.show_id.in_(hall_show_ids),
                    Booking.status == "confirmed"
                )
            ).scalar() or 0
            
            # Get revenue for this hall
            hall_revenue = db.query(func.sum(Booking.amount_paid)).filter(
                and_(
                    Booking.show_id.in_(hall_show_ids),
                    Booking.status == "confirmed"
                )
            ).scalar() or 0.0
            
            # Calculate occupancy
            occupancy = (booked_seats / total_seats * 100) if total_seats > 0 else 0
            
            halls_data.append({
                "hall_id": hall.id,
                "hall_name": hall.name,
                "total_shows": len(hall_shows),
                "total_seats": total_seats,
                "booked_seats": booked_seats,
                "revenue": float(hall_revenue),
                "occupancy_percentage": round(occupancy, 2)
            })
            
            total_seats_available += total_seats
            total_booked_seats += booked_seats
    
    # Calculate average occupancy
    average_occupancy = (total_booked_seats / total_seats_available * 100) if total_seats_available > 0 else 0
    
    return TheaterAnalyticsResponse(
        theater_id=theater_id,
        theater_name=theater.name,
        period_start=start_date,
        period_end=end_date,
        total_halls=len(halls),
        total_shows=len(shows),
        total_bookings=booking_stats.total_bookings or 0,
        total_revenue=float(booking_stats.total_revenue or 0),
        average_occupancy=round(average_occupancy, 2),
        halls_data=halls_data
    )

@router.get("/revenue", response_model=RevenueAnalyticsResponse)
def get_revenue_analytics(
    start_date: Optional[date] = Query(None, description="Start date for analytics (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for analytics (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get overall revenue analytics."""
    
    # Set default date range if not provided (last 30 days)
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get all shows in the date range
    shows = db.query(Show).filter(
        and_(
            Show.show_date >= start_date,
            Show.show_date <= end_date
        )
    ).all()
    
    show_ids = [show.id for show in shows]
    
    if not show_ids:
        return RevenueAnalyticsResponse(
            period_start=start_date,
            period_end=end_date,
            total_revenue=0.0,
            total_bookings=0,
            average_booking_value=0.0,
            daily_revenue=[],
            movie_revenue=[],
            theater_revenue=[]
        )
    
    # Get overall revenue statistics
    revenue_stats = db.query(
        func.sum(Booking.amount_paid).label('total_revenue'),
        func.count(Booking.id).label('total_bookings'),
        func.avg(Booking.amount_paid).label('average_booking_value')
    ).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).first()
    
    # Get daily revenue breakdown
    daily_revenue = db.query(
        Booking.booking_date,
        func.sum(Booking.amount_paid).label('daily_revenue'),
        func.count(Booking.id).label('daily_bookings')
    ).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).group_by(Booking.booking_date).order_by(Booking.booking_date).all()
    
    daily_revenue_data = [
        {
            "date": str(item.booking_date),
            "revenue": float(item.daily_revenue),
            "bookings": item.daily_bookings
        }
        for item in daily_revenue
    ]
    
    # Get movie-wise revenue
    movie_revenue = db.query(
        Movie.title,
        func.sum(Booking.amount_paid).label('movie_revenue'),
        func.count(Booking.id).label('movie_bookings')
    ).join(Show, Show.movie_id == Movie.id).join(Booking, Booking.show_id == Show.id).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).group_by(Movie.title).order_by(desc(func.sum(Booking.amount_paid))).all()
    
    movie_revenue_data = [
        {
            "movie_title": item.title,
            "revenue": float(item.movie_revenue),
            "bookings": item.movie_bookings
        }
        for item in movie_revenue
    ]
    
    # Get theater-wise revenue
    theater_revenue = db.query(
        Theater.name,
        func.sum(Booking.amount_paid).label('theater_revenue'),
        func.count(Booking.id).label('theater_bookings')
    ).join(Hall, Hall.theater_id == Theater.id).join(Show, Show.hall_id == Hall.id).join(Booking, Booking.show_id == Show.id).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).group_by(Theater.name).order_by(desc(func.sum(Booking.amount_paid))).all()
    
    theater_revenue_data = [
        {
            "theater_name": item.name,
            "revenue": float(item.theater_revenue),
            "bookings": item.theater_bookings
        }
        for item in theater_revenue
    ]
    
    return RevenueAnalyticsResponse(
        period_start=start_date,
        period_end=end_date,
        total_revenue=float(revenue_stats.total_revenue or 0),
        total_bookings=revenue_stats.total_bookings or 0,
        average_booking_value=float(revenue_stats.average_booking_value or 0),
        daily_revenue=daily_revenue_data,
        movie_revenue=movie_revenue_data,
        theater_revenue=theater_revenue_data
    )

@router.get("/top-movies", response_model=List[TopMoviesResponse])
def get_top_movies(
    limit: int = Query(10, description="Number of top movies to return"),
    start_date: Optional[date] = Query(None, description="Start date for analytics (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for analytics (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get top performing movies by revenue and bookings."""
    
    # Set default date range if not provided (last 30 days)
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get all shows in the date range
    shows = db.query(Show).filter(
        and_(
            Show.show_date >= start_date,
            Show.show_date <= end_date
        )
    ).all()
    
    show_ids = [show.id for show in shows]
    
    if not show_ids:
        return []
    
    # Get top movies by revenue
    top_movies = db.query(
        Movie.id,
        Movie.title,
        Movie.genre,
        func.sum(Booking.amount_paid).label('total_revenue'),
        func.count(Booking.id).label('total_bookings'),
        func.avg(Booking.amount_paid).label('average_booking_value')
    ).join(Show, Show.movie_id == Movie.id).join(Booking, Booking.show_id == Show.id).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).group_by(Movie.id, Movie.title, Movie.genre).order_by(desc(func.sum(Booking.amount_paid))).limit(limit).all()
    
    return [
        TopMoviesResponse(
            movie_id=item.id,
            movie_title=item.title,
            genre=item.genre,
            total_revenue=float(item.total_revenue),
            total_bookings=item.total_bookings,
            average_booking_value=float(item.average_booking_value)
        )
        for item in top_movies
    ]

@router.get("/top-theaters", response_model=List[TopTheatersResponse])
def get_top_theaters(
    limit: int = Query(10, description="Number of top theaters to return"),
    start_date: Optional[date] = Query(None, description="Start date for analytics (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for analytics (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get top performing theaters by revenue and bookings."""
    
    # Set default date range if not provided (last 30 days)
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get all shows in the date range
    shows = db.query(Show).filter(
        and_(
            Show.show_date >= start_date,
            Show.show_date <= end_date
        )
    ).all()
    
    show_ids = [show.id for show in shows]
    
    if not show_ids:
        return []
    
    # Get top theaters by revenue
    top_theaters = db.query(
        Theater.id,
        Theater.name,
        Theater.city,
        func.sum(Booking.amount_paid).label('total_revenue'),
        func.count(Booking.id).label('total_bookings'),
        func.avg(Booking.amount_paid).label('average_booking_value')
    ).join(Hall, Hall.theater_id == Theater.id).join(Show, Show.hall_id == Hall.id).join(Booking, Booking.show_id == Show.id).filter(
        and_(
            Booking.show_id.in_(show_ids),
            Booking.status == "confirmed"
        )
    ).group_by(Theater.id, Theater.name, Theater.city).order_by(desc(func.sum(Booking.amount_paid))).limit(limit).all()
    
    return [
        TopTheatersResponse(
            theater_id=item.id,
            theater_name=item.name,
            city=item.city,
            total_revenue=float(item.total_revenue),
            total_bookings=item.total_bookings,
            average_booking_value=float(item.average_booking_value)
        )
        for item in top_theaters
    ]

@router.get("/seat-utilization", response_model=SeatUtilizationResponse)
def get_seat_utilization(
    start_date: Optional[date] = Query(None, description="Start date for analytics (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for analytics (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get seat utilization analytics across all halls."""
    
    # Set default date range if not provided (last 30 days)
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    # Get all shows in the date range
    shows = db.query(Show).filter(
        and_(
            Show.show_date >= start_date,
            Show.show_date <= end_date
        )
    ).all()
    
    show_ids = [show.id for show in shows]
    
    if not show_ids:
        return SeatUtilizationResponse(
            period_start=start_date,
            period_end=end_date,
            total_shows=0,
            total_seats_available=0,
            total_seats_booked=0,
            overall_utilization=0.0,
            hall_utilization=[]
        )
    
    # Calculate overall utilization
    total_seats_available = 0
    total_seats_booked = 0
    hall_utilization_data = []
    
    # Get all halls
    halls = db.query(Hall).all()
    
    for hall in halls:
        # Get shows for this hall
        hall_shows = [show for show in shows if show.hall_id == hall.id]
        hall_show_ids = [show.id for show in hall_shows]
        
        if hall_show_ids:
            # Get total seats in this hall
            total_seats = db.query(func.count(Booking.id)).filter(
                Booking.show_id.in_(hall_show_ids)
            ).scalar() or 0
            
            # Get booked seats for this hall
            booked_seats = db.query(func.count(Booking.id)).filter(
                and_(
                    Booking.show_id.in_(hall_show_ids),
                    Booking.status == "confirmed"
                )
            ).scalar() or 0
            
            # Calculate utilization
            utilization = (booked_seats / total_seats * 100) if total_seats > 0 else 0
            
            hall_utilization_data.append({
                "hall_id": hall.id,
                "hall_name": hall.name,
                "theater_name": hall.theater.name if hall.theater else "Unknown",
                "total_shows": len(hall_shows),
                "total_seats": total_seats,
                "booked_seats": booked_seats,
                "utilization_percentage": round(utilization, 2)
            })
            
            total_seats_available += total_seats
            total_seats_booked += booked_seats
    
    # Calculate overall utilization
    overall_utilization = (total_seats_booked / total_seats_available * 100) if total_seats_available > 0 else 0
    
    return SeatUtilizationResponse(
        period_start=start_date,
        period_end=end_date,
        total_shows=len(shows),
        total_seats_available=total_seats_available,
        total_seats_booked=total_seats_booked,
        overall_utilization=round(overall_utilization, 2),
        hall_utilization=hall_utilization_data
    )

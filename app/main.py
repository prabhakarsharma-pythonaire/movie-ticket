from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.core.database import Base
from app.api import movies, theaters, halls, seats, shows, bookings, users, analytics
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="A comprehensive movie ticket booking system API with advanced analytics"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(movies.router, prefix=settings.API_V1_STR, tags=["movies"])
app.include_router(theaters.router, prefix=settings.API_V1_STR, tags=["theaters"])
app.include_router(halls.router, prefix=settings.API_V1_STR, tags=["halls"])
app.include_router(seats.router, prefix=settings.API_V1_STR, tags=["seats"])
app.include_router(shows.router, prefix=settings.API_V1_STR, tags=["shows"])
app.include_router(bookings.router, prefix=settings.API_V1_STR, tags=["bookings"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(analytics.router, prefix=settings.API_V1_STR, tags=["analytics"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Movie Booking System API with Advanced Analytics",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "Movie & Theater Management",
            "Flexible Seat Layout System",
            "Show Scheduling",
            "User Management",
            "Single & Group Booking",
            "Consecutive Seat Booking",
            "Alternative Booking Suggestions",
            "Advanced Analytics & Reporting"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

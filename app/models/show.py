from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Show(Base):
    __tablename__ = "shows"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    show_date = Column(DateTime, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    price_multiplier = Column(Float, default=1.0)  # Multiplier for base movie price
    status = Column(String(20), default="active")  # active, cancelled, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    movie = relationship("Movie", back_populates="shows")
    hall = relationship("Hall", back_populates="shows")
    bookings = relationship("Booking", back_populates="show")
    
    def __repr__(self):
        return f"<Show(id={self.id}, movie_id={self.movie_id}, hall_id={self.hall_id}, date={self.show_date})>"

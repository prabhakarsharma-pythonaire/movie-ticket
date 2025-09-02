from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True)
    hall_id = Column(Integer, ForeignKey("halls.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)  # Column number within the row
    seat_type = Column(String(20), default="standard")  # standard, premium, etc.
    is_aisle = Column(Boolean, default=False)  # True if it's an aisle seat
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    hall = relationship("Hall", back_populates="seats")
    bookings = relationship("Booking", back_populates="seat")
    
    def __repr__(self):
        return f"<Seat(id={self.id}, hall_id={self.hall_id}, row={self.row_number}, seat={self.seat_number})>"

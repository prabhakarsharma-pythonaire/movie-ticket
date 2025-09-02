from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Theater(Base):
    __tablename__ = "theaters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    contact_number = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    halls = relationship("Hall", back_populates="theater")
    
    def __repr__(self):
        return f"<Theater(id={self.id}, name='{self.name}')>"

class Hall(Base):
    __tablename__ = "halls"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    total_rows = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    theater = relationship("Theater", back_populates="halls")
    seats = relationship("Seat", back_populates="hall")
    shows = relationship("Show", back_populates="hall")
    
    def __repr__(self):
        return f"<Hall(id={self.id}, name='{self.name}', theater_id={self.theater_id})>"

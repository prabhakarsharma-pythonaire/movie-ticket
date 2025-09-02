from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.theater import Theater
from app.schemas.theater import TheaterCreate, TheaterUpdate, TheaterResponse

router = APIRouter(prefix="/theaters", tags=["theaters"])

@router.post("/", response_model=TheaterResponse, status_code=status.HTTP_201_CREATED)
def create_theater(theater: TheaterCreate, db: Session = Depends(get_db)):
    """Create a new theater."""
    db_theater = Theater(**theater.dict())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater

@router.get("/", response_model=List[TheaterResponse])
def get_theaters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all theaters with pagination."""
    theaters = db.query(Theater).offset(skip).limit(limit).all()
    return theaters

@router.get("/{theater_id}", response_model=TheaterResponse)
def get_theater(theater_id: int, db: Session = Depends(get_db)):
    """Get a specific theater by ID."""
    theater = db.query(Theater).filter(Theater.id == theater_id).first()
    if theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater

@router.put("/{theater_id}", response_model=TheaterResponse)
def update_theater(theater_id: int, theater: TheaterUpdate, db: Session = Depends(get_db)):
    """Update a theater."""
    db_theater = db.query(Theater).filter(Theater.id == theater_id).first()
    if db_theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    
    update_data = theater.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_theater, field, value)
    
    db.commit()
    db.refresh(db_theater)
    return db_theater

@router.delete("/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_theater(theater_id: int, db: Session = Depends(get_db)):
    """Delete a theater."""
    db_theater = db.query(Theater).filter(Theater.id == theater_id).first()
    if db_theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")
    
    db.delete(db_theater)
    db.commit()
    return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.theater import Hall
from app.schemas.theater import HallCreate, HallUpdate, HallResponse

router = APIRouter(prefix="/halls", tags=["halls"])

@router.post("/", response_model=HallResponse, status_code=status.HTTP_201_CREATED)
def create_hall(hall: HallCreate, db: Session = Depends(get_db)):
    """Create a new hall."""
    db_hall = Hall(**hall.dict())
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall

@router.get("/", response_model=List[HallResponse])
def get_halls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all halls with pagination."""
    halls = db.query(Hall).offset(skip).limit(limit).all()
    return halls

@router.get("/{hall_id}", response_model=HallResponse)
def get_hall(hall_id: int, db: Session = Depends(get_db)):
    """Get a specific hall by ID."""
    hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if hall is None:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall

@router.get("/theater/{theater_id}", response_model=List[HallResponse])
def get_halls_by_theater(theater_id: int, db: Session = Depends(get_db)):
    """Get all halls for a specific theater."""
    halls = db.query(Hall).filter(Hall.theater_id == theater_id).all()
    return halls

@router.put("/{hall_id}", response_model=HallResponse)
def update_hall(hall_id: int, hall: HallUpdate, db: Session = Depends(get_db)):
    """Update a hall."""
    db_hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if db_hall is None:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    update_data = hall.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hall, field, value)
    
    db.commit()
    db.refresh(db_hall)
    return db_hall

@router.delete("/{hall_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hall(hall_id: int, db: Session = Depends(get_db)):
    """Delete a hall."""
    db_hall = db.query(Hall).filter(Hall.id == hall_id).first()
    if db_hall is None:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    db.delete(db_hall)
    db.commit()
    return None

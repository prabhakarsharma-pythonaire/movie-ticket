from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.show import Show
from app.models.movie import Movie
from app.models.theater import Hall
from app.schemas.show import ShowCreate, ShowUpdate, ShowResponse

router = APIRouter(prefix="/shows", tags=["shows"])

@router.post("/", response_model=ShowResponse, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowCreate, db: Session = Depends(get_db)):
    """Create a new show."""
    # Verify movie exists
    movie = db.query(Movie).filter(Movie.id == show.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Verify hall exists
    hall = db.query(Hall).filter(Hall.id == show.hall_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    
    db_show = Show(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

@router.get("/", response_model=List[ShowResponse])
def get_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all shows with pagination."""
    shows = db.query(Show).offset(skip).limit(limit).all()
    return shows

@router.get("/movie/{movie_id}", response_model=List[ShowResponse])
def get_shows_by_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get all shows for a specific movie."""
    shows = db.query(Show).filter(Show.movie_id == movie_id).all()
    return shows

@router.get("/hall/{hall_id}", response_model=List[ShowResponse])
def get_shows_by_hall(hall_id: int, db: Session = Depends(get_db)):
    """Get all shows for a specific hall."""
    shows = db.query(Show).filter(Show.hall_id == hall_id).all()
    return shows

@router.get("/{show_id}", response_model=ShowResponse)
def get_show(show_id: int, db: Session = Depends(get_db)):
    """Get a specific show by ID."""
    show = db.query(Show).filter(Show.id == show_id).first()
    if show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    return show

@router.put("/{show_id}", response_model=ShowResponse)
def update_show(show_id: int, show: ShowUpdate, db: Session = Depends(get_db)):
    """Update a show."""
    db_show = db.query(Show).filter(Show.id == show_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    
    update_data = show.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_show, field, value)
    
    db.commit()
    db.refresh(db_show)
    return db_show

@router.delete("/{show_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_show(show_id: int, db: Session = Depends(get_db)):
    """Delete a show."""
    db_show = db.query(Show).filter(Show.id == show_id).first()
    if db_show is None:
        raise HTTPException(status_code=404, detail="Show not found")
    
    db.delete(db_show)
    db.commit()
    return None

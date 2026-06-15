from fastapi import APIRouter, HTTPException, status, Depends
from app.services.user_service import create_user
from app.database import get_db
from app.auth import password_hash
from app.schemas import UserCreate

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError



router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    hashed_password = password_hash(user.password)

    try:
        create_user(db, user.username, hashed_password)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    return {
        "status": "Registered"
    }
    
    



from fastapi import APIRouter, HTTPException, Depends
from app.services.user_service import get_user 
from app.database import get_db
from app.auth import verify_password, create_acess_token
from app.schemas import UserCreate
from app.redis_client import redis_client

from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    attempts = redis_client.get(user.username)

    if attempts and int(attempts) >= 5:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts"
        )

    stored_user = get_user(db, user.username)

    if stored_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credential"
        )

    try:
        verify_password(user.password, stored_user.password)
    
    except HTTPException:
        redis_client.incr(user.username)
        redis_client.expire(user.username, 30)
        # re-raise try block exception
        raise

    redis_client.delete(user.username)

    token = create_acess_token(stored_user.username)

    return {
        "status": "login success",
        "access_token": token 
    }

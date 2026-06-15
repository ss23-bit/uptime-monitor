from app.models.user import User
from app.database import SessionLocal

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, username: str, password: str,):

    user = User(
        username=username,
        password=password
    )
    db.add(user)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    
def get_user(db: Session, username: str):

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )
    
    return user


    
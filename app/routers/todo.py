from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.services.todo_service import get_stored_todo, store_todo, update_stored_todo, delete_stored_todo
from app.services.user_service import get_user
from app.database import get_db
from app.schemas import ToDo
from app.auth import verify_access_token

from sqlalchemy.orm import Session 

router = APIRouter()

def not_authenticated():
    raise HTTPException(
        status_code=401,
        detail="Not authenticated"
    )

@router.get("/todos")
def get_todo(
    search: str | None = None,
    limit: int = Query(default=10, le=100),
    offset: int = 0,
    db: Session = Depends(get_db), 
    username: str = Depends(verify_access_token)
    ):
    
    user = get_user(db, username)
    if user is None:
        raise not_authenticated()
    
    return get_stored_todo(
        db, 
        user.id,
        search,
        limit,
        offset
        )
    

@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: ToDo,
    db: Session = Depends(get_db),
    username: str = Depends(verify_access_token)
    ):

    user = get_user(db, username)
    if user is None:
        raise not_authenticated()

    return store_todo(db, todo.title, user.id) 

@router.put("/todos/{todo_id}")
def update_todo(
    todo: ToDo,
    todo_id: int,
    db: Session = Depends(get_db), 
    username: str = Depends(verify_access_token)
    ):

    user = get_user(db, username)
    if user is None:
        raise not_authenticated()

    return update_stored_todo(db, todo.title, todo_id, user.id)

@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db), 
    username: str = Depends(verify_access_token)
    ):

    user = get_user(db, username)
    if user is None:
        raise not_authenticated()

    return delete_stored_todo(db, todo_id, user.id)
    
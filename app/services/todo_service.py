from fastapi import HTTPException, Depends
from app.database import get_db
from app.models.todo import Todo

from sqlalchemy.orm import Session

def get_stored_todo(
        db: Session, 
        user_id: int,
        search: str | None, 
        limit: int, 
        offset: int):
    
    query = (
        db.query(Todo)
        .filter(Todo.user_id == user_id)
    )

    if search:
        query = query.filter(
            Todo.title.ilike(f"%{search}%")
        )
    
    todos = (
        query
        .limit(limit)
        .offset(offset)
        .all()
    )
        
    return todos

def store_todo(db: Session, todo_title: str, user_id: int):

    if not todo_title:
        raise HTTPException(
            status_code=400,
            detail="title cannot be empty"
        )
    
    title = Todo(
        title=todo_title,
        user_id=user_id
    )

    db.add(title)
    db.commit()

    return {
        "status": "created"
    }

def update_stored_todo(
        db: Session,
        title: str, 
        todo_id: int, 
        user_id: int,
        ):
    
    todo = (
        db.query(Todo)
        .filter(
            Todo.id == todo_id,
            Todo.user_id == user_id
        )
        .first()
    )
    
    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )
    
    todo.title = title

    db.commit()
    db.refresh(todo)

    return {
        "status": "updated",
        "data": {
            "id": todo.id,
            "title": todo.title
        }
    }

def delete_stored_todo(db: Session, todo_id: int, user_id: int):
    
    todo = (
        db.query(Todo)
        .filter(
            Todo.id == todo_id,
            Todo.user_id == user_id
        )
        .first()
    )

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return {
        "status": "deleted"
    }
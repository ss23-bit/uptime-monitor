from __future__ import annotations
from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.todo import Todo

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(   
        primary_key=True
    )
    
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    
    password: Mapped[str] = mapped_column(
        nullable=False
    )

    todos: Mapped[list["Todo"]] = relationship(
        back_populates="user"
    )
from pydantic import BaseModel, EmailStr
from typing import List
from app.schemas.todo import Todo


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserWithTodos(User):
    todos: List[Todo] = []

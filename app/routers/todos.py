from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.todo import Todo
from app.models.user import User
import app.schemas
from app.tracer import get_tracer
from opentelemetry.trace.status import Status, StatusCode


todoRouter = APIRouter(tags=["todos"])
tracer = get_tracer("todos")


@todoRouter.post("/todos/", response_model=app.schemas.Todo)
def create_todo(
    todo: app.schemas.TodoCreate, user_id: int, db: Session = Depends(get_db)
):
    with tracer.start_as_current_span("create_todo") as span:
        span.set_attribute("todo.title", todo.title)
        span.set_attribute("user.id", user_id)
        with tracer.start_as_current_span("fetch_user_from_db"):
            user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="user not found")
        with tracer.start_as_current_span("create_db_todo") as span:
            try:
                db_todo = Todo(**todo.model_dump(), user_id=user_id)
                db.add(db_todo)
                db.commit()
                db.refresh(db_todo)
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise HTTPException(status_code=500, detail="Failed to create todo")
    return db_todo


@todoRouter.get("/todos/", response_model=List[app.schemas.Todo])
def get_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Todo).offset(skip).limit(limit).all()


@todoRouter.get("/todos/{todo_id}", response_model=app.schemas.Todo)
def read_todo(
    todo_id: int, todo_update: app.schemas.TodoUpdate, db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    for var, value in vars(todo_update).items():
        if value:
            setattr(todo, var, value)
    db.commit()
    db.refresh(todo)
    return todo


@todoRouter.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"detail": "todo deleted"}

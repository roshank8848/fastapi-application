from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models
import app.schemas
from app.database import get_db

userRouter = APIRouter(tags=["users"])


@userRouter.post("/users/", response_model=app.schemas.User)
def create_user(user: app.schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = app.models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@userRouter.get("/users/", response_model=list[app.schemas.User])
def get_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(app.models.User).offset(skip).limit(limit).all()


@userRouter.get("/users/{user_id}", response_model=app.schemas.UserWithTodos)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(app.models.User).filter(app.models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@userRouter.put("/users/{user_id}", response_model=app.schemas.User)
def update_user(
    user_id: int, user_update: app.schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = db.query(app.models.User).filter(app.models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    if user_update is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    db.commit()
    db.refresh(user)
    return user


@userRouter.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(app.models.User).filter(app.models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(user)
    db.commit()
    return {"detail": "user deleted"}

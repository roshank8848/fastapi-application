from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users_router, todos_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(todos_router)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI app with routers!"}

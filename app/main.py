from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users_router, todos_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(todos_router)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI app with routers!"}

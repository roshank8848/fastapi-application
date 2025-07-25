from fastapi import FastAPI, Depends, Request
from app.routers import users_router, todos_router
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.auth.jwtvalidation import get_current_user
from app.schemas.tokendata import TokenData
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import engine, Base
from app.auth.jwtvalidation import require_roles


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/app")
Instrumentator().instrument(app).expose(app)

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


@app.get("/secure")
async def secure_endpoint(current_user: TokenData = Depends(get_current_user)):
    return {"message": "This is a secure endpoint", "current_user": current_user}


@app.get("/")
def root(user: TokenData = Depends(require_roles(["role_user"]))):
    return {"message": "Welcome to the FastAPI app with routers! You are authenticated.", "user": user}


@app.get("/headers")
async def headers_endpoint(request: Request):
    return {"headers": request.headers}

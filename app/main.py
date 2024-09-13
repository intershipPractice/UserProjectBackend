from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app import models
from contextlib import asynccontextmanager
from app.user import routes as user_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.SQLModel.metadata.create_all(models.engine)
    yield

app = FastAPI(lifespan=lifespan)
router = APIRouter(prefix="/api/v1")
app.include_router(user_routes.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

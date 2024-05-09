from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.api import router as api_router
from app.core.config import settings
from app.db.init_db import get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_db()
    yield


app = FastAPI(
    title="Monitor Microservice",
    lifespan=lifespan,
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

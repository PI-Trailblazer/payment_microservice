from app.api import deps
from fastapi import APIRouter, Depends, HTTPException, Security, Cookie, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional

# from app import crud
# from app.schemas import PaymentCreate

# from app.schemas.payment import PaymentInDB

router = APIRouter()


@router.get("/", response_model=str)
def read_root():
    return "Hello World"

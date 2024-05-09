from fastapi import APIRouter

from . import payment

router = APIRouter()

router.include_router(payment.router, prefix="/payment", tags=["payment"])

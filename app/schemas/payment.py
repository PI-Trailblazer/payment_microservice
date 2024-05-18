from pydantic import BaseModel
from typing import Optional
from datetime import datetime as Datetime


class Transaction(BaseModel):
    userid: str
    amount: float
    quantity: int
    status: str
    offer_id: int
    nationality: str


class TransactionCreate(Transaction):
    offer_id: int


class TransactionUpdate(Transaction):
    userid: str
    amount: float
    quantity: int
    status: str
    offer_id: int
    nationality: str


class TransactionInDB(Transaction):
    id: int
    timestamp: Optional[Datetime]

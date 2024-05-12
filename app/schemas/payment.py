from pydantic import BaseModel


class Transaction(BaseModel):
    userid: str
    amount: float
    quantity: int
    timesatmp: str
    status: str
    offer_id: int
    nationality: str


class TransactionCreate(Transaction):
    offer_id: int


class TransactionUpdate(Transaction):
    userid: str
    amount: float
    quantity: int
    timesatmp: str
    status: str
    offer_id: int
    nationality: str


class TransactionInDB(Transaction):
    id: int

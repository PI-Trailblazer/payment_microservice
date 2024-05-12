from fastapi import APIRouter, Depends, HTTPException, Security, Cookie, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from requests import Session
from fastapi.params import Query
from typing import List, Optional
from app import crud
from app.api import deps
from app.schemas import (
    Transaction,
    TransactionCreate,
    TransactionUpdate,
    TransactionInDB,
)

router = APIRouter()


# Needs authorization
@router.post("/", response_model=Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction: TransactionCreate,
    headers: deps.AuthHeader = Depends(deps.get_auth_header),
) -> Transaction:
    id_token = headers.Authorization[7:]
    uid = deps.decode_token(id_token)["user_id"]
    transaction.userid = uid
    return crud.transaction.create(db, obj_in=transaction)


# Needs authorization
@router.get("/", response_model=List[TransactionInDB])
def get_transactions(db: Session = Depends(deps.get_db)) -> List[TransactionInDB]:
    return crud.transaction.get_all_transactions(db)


# Needs authorization
@router.get("/{id}")
def get_transaction_by_id(
    *, db: Session = Depends(deps.get_db), id: int
) -> Optional[TransactionInDB]:
    transaction = crud.transaction.get(db, id=id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


# Needs authorization
@router.get("/user/")
def get_transactions_by_userid(
    *,
    db: Session = Depends(deps.get_db),
    headers: deps.AuthHeader = Depends(deps.get_auth_header),
) -> List[TransactionInDB]:
    id_token = headers.Authorization[7:]
    uid = deps.decode_token(id_token)["user_id"]
    return crud.transaction.get_transactions_by_userid(db, uid)

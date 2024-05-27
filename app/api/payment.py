import json
from fastapi import APIRouter, Depends, HTTPException, Security, Cookie, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from requests import Session
from fastapi.params import Query
from typing import List, Optional
from app import crud
from app.api import auth_deps, deps
from app.schemas import (
    Transaction,
    TransactionCreate,
    TransactionUpdate,
    TransactionInDB,
)
import pika

router = APIRouter()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq",
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials(username="user", password="user"),
    )
)

channel = connection.channel()
channel.queue_declare(queue="purchased_offers")


# Needs authorization
@router.post("/", response_model=Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction: TransactionCreate,
    payload=Security(auth_deps.verify_token, scopes=[]),
) -> Transaction:
    uid = payload.sub

    transaction.userid = uid
    transaction = crud.transaction.create(db, obj_in=transaction)

    body = json.dumps({"offer_id": transaction.offer_id})
    channel.basic_publish(
        exchange="",
        routing_key="purchased_offers",
        body=body,
    )

    return transaction


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
    payload=Security(auth_deps.verify_token, scopes=[]),
) -> List[TransactionInDB]:
    uid = payload.sub
    return crud.transaction.get_transactions_by_userid(db, uid)


@router.delete("/")
def delete_all_transactions(db: Session = Depends(deps.get_db)):
    crud.transaction.delete_all_transactions(db)
    return Response(status_code=204)

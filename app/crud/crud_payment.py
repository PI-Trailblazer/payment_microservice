from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.payment import Transaction
from app.schemas.payment import TransactionCreate, TransactionUpdate
import pika
from fastapi.encoders import jsonable_encoder
from datetime import datetime as Datetime
import json


class CRUDPayment(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def create(self, db: Session, *, obj_in: TransactionCreate) -> Transaction:

        db_obj = super().create(db, obj_in=obj_in)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq",
                port=5672,
                virtual_host="/",
                credentials=pika.PlainCredentials(username="user", password="user"),
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue="payment")

        payment_dict = jsonable_encoder(obj_in)
        payment_dict["timestamp"] = Datetime.now().isoformat()
        body = json.dumps(payment_dict)

        channel.basic_publish(
            exchange="",
            routing_key="payment",
            body=body,
        )

        connection.close()

        return db_obj

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",
            port=5672,
            virtual_host="/",
            credentials=pika.PlainCredentials(username="user", password="user"),
        )
    )

    def update(
        self, db: Session, *, db_obj: Transaction, obj_in: TransactionUpdate
    ) -> Transaction:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def get_transaction_by_id(self, db: Session, payment_id: int) -> Transaction:
        return db.query(self.model).filter(self.model.id == payment_id).first()

    def get_transactions_by_userid(
        self, db: Session, user_id: str
    ) -> list[Transaction]:
        return db.query(self.model).filter(self.model.userid == user_id).all()

    def delete_all_transactions(self, db: Session) -> None:
        db.query(self.model).delete()
        db.commit()

    def get_transactions_by_offer_id(
        self, db: Session, offer_id: int
    ) -> list[Transaction]:
        return db.query(self.model).filter(self.model.offer_id == offer_id).all()

    def get_transactions_by_status(self, db: Session, status: str) -> list[Transaction]:
        return db.query(self.model).filter(self.model.status == status).all()

    def get_transactions_by_nationality(
        self, db: Session, status: str
    ) -> list[Transaction]:
        return db.query(self.model).filter(self.model.nationality == status).all()

    def get_all_transactions(self, db: Session) -> list[Transaction]:
        return db.query(self.model).all()


transaction = CRUDPayment(Transaction)

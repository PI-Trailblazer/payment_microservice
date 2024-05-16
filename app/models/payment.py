from typing import Optional
from typing import List

from sqlalchemy import String, Integer, Boolean, Float, ARRAY, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

from datetime import datetime
from sqlalchemy import DateTime


class Transaction(Base):
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    userid: Mapped[str] = mapped_column(String(128), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )
    status: Mapped[str] = mapped_column(String(128), nullable=False)
    offer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    nationality: Mapped[str] = mapped_column(String(128), nullable=False)

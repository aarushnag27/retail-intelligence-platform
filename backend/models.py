from sqlalchemy import ForeignKey, String, Integer, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    barcode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    sold_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    transaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("transactions.transaction_id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
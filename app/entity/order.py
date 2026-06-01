from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entity.base import Base


class OrderStatus(Base):
    """Статус заказа"""
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    # orders: Mapped[List["Order"]] = relationship(back_populates="status")


class Order(Base):
    """Заказ"""
    __tablename__ = "orders"

    # TODO: article

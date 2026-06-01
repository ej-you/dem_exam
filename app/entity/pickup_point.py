from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.entity.base import Base


class PickupPoint(Base):
    """Пункт выдачи заказов"""
    __tablename__ = "pickup_points"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # TODO: relationship for order

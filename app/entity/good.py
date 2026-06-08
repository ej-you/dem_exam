from typing import List

from sqlalchemy import String, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entity.base import Base, RESTRICT
from config.config import DEFAULT_PHOTO_PATH


class MeasurementUnit(Base):
    """Единица измерения"""
    __tablename__ = "measurement_units"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)

    goods: Mapped[List["Good"]] = relationship(back_populates="measurement_unit")


# class Supplier(Base):
#     """Поставщик"""
#     __tablename__ = "suppliers"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(50), nullable=False)
#
#     goods: Mapped[List["Good"]] = relationship(back_populates="supplier")
#
#
# class Producer(Base):
#     """Производитель"""
#     __tablename__ = "producers"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(50), nullable=False)
#
#     goods: Mapped[List["Good"]] = relationship(back_populates="producer")


class Company(Base):
    """Компания"""
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # goods: Mapped[List["Good"]] = relationship(back_populates="producer")

    supplied_goods: Mapped[List["Good"]] = relationship(
        "Good",
        foreign_keys="[Good.supplier_id]",
        back_populates="supplier"
    )
    produced_goods: Mapped[List["Good"]] = relationship(
        "Good",
        foreign_keys="[Good.producer_id]",
        back_populates="producer"
    )


class GoodCategory(Base):
    """Категория товара"""
    __tablename__ = "good_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(35), nullable=False)

    goods: Mapped[List["Good"]] = relationship(back_populates="good_category")


class Good(Base):
    """Товар"""
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    article: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    measurement_unit_id: Mapped[int] = mapped_column(
        ForeignKey("measurement_units.id", ondelete=RESTRICT), nullable=False
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    # supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id", ondelete=RESTRICT), nullable=False)
    # producer_id: Mapped[int] = mapped_column(ForeignKey("producer.id", ondelete=RESTRICT), nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete=RESTRICT), nullable=False)
    producer_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete=RESTRICT), nullable=False)
    good_category_id: Mapped[int] = mapped_column(
        ForeignKey("good_categories.id", ondelete=RESTRICT), nullable=False
    )
    discount: Mapped[int] = mapped_column(default=0, nullable=False)
    amount: Mapped[int] = mapped_column(default=0, nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    photo: Mapped[str] = mapped_column(String(255), default=DEFAULT_PHOTO_PATH, nullable=False)

    measurement_unit: Mapped["MeasurementUnit"] = relationship(back_populates="goods")
    good_category: Mapped["GoodCategory"] = relationship(back_populates="goods")
    # supplier: Mapped["Supplier"] = relationship(back_populates="goods")
    # producer: Mapped["Producer"] = relationship(back_populates="goods")

    supplier: Mapped["Company"] = relationship(
        "Company",
        foreign_keys=[supplier_id],
        back_populates="supplied_goods"
    )
    producer: Mapped["Company"] = relationship(
        "Company",
        foreign_keys=[producer_id],
        back_populates="produced_goods"
    )

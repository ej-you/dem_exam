from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entity.base import Base, RESTRICT


class Role(Base):
    """Роль пользователя"""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="role")


class User(Base):
    """Пользователь"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete=RESTRICT), nullable=False)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped["Role"] = relationship(back_populates="users")
    # TODO: relationship for order

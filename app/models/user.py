from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cart import UserCart

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index = True
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique = True,
        nullable = False
    )
    email : Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )
    phone: Mapped[str] = mapped_column(String(15))

    cart:Mapped["UserCart"] = relationship(
        back_populates="user",
        
    )
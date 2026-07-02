from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class UserCart(Base):
    __tablename__ = "user_carts"

    id:Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    user:Mapped["User"] = relationship(
        back_populates="cart"
    )

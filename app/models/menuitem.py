from sqlalchemy import Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.category import Category

class MenuItem(Base):
    __tablename__ = "menu_items"

    id:Mapped[int] = mapped_column(
       
        primary_key=True,
        
    )
    name:Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description:Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    price:Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    image_url:Mapped[str | None]= mapped_column(
        String(255),
        nullable=True
    )
    is_available:Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    category_id:Mapped[int] = mapped_column(
        ForeignKey("categories.id"),

        nullable=False
    )
    stock:Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    category:Mapped["Category"] = relationship(
        back_populates="menu_items"
    )
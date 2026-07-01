from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.menuitem import MenuItem

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
       
        primary_key=True,
        
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique = True,
        nullable = False
    )
    description : Mapped[str | None] = mapped_column(
        String(255),
        nullable = True
    )
    menu_items: Mapped[list["MenuItem"]] = relationship(
    back_populates="category"
    )
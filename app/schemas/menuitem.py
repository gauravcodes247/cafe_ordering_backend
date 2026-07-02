from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from app.schemas.category import CategorySummary

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    image_url: str
    is_available: bool = True
    category_id: int
    stock: int


class MenuItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    is_available: bool | None = None
    category_id: int | None = None
    stock: int | None = None


class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    image_url: str
    is_available: bool
    stock: int
    category:CategorySummary
    model_config = ConfigDict(from_attributes=True)

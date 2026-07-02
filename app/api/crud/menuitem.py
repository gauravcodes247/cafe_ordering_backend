from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.dependecis import get_db
from app.models.menuitem import MenuItem
from app.models.category import Category
from app.schemas.menuitem import MenuItemCreate, MenuItemResponse, MenuItemUpdate


router = APIRouter(
    prefix="/menu-item",
    tags=["Menu Items"]
)

# Create menu item


@router.post("", response_model=MenuItemResponse)
def create_menuItem(menu_item: MenuItemCreate, db: Session = Depends(get_db)):
    category = db.scalar(select(Category).where(
        Category.id == menu_item.category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This Category Doesn't exists"
        )

    item = db.scalar(select(MenuItem).where(
        MenuItem.name == menu_item.name))
    if item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Menu Item Already Exists"
        )

    db_item = MenuItem(
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        image_url=menu_item.image_url,
        is_available=menu_item.is_available,
        category_id=menu_item.category_id,
        stock=menu_item.stock

    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

# get all menu items


@router.get("", response_model=list[MenuItemResponse])
def get_menuItems(db: Session = Depends(get_db)):
    all_items = db.scalars(select(MenuItem)).all()

    return all_items

# get item by id


@router.get("/{id}", response_model=MenuItemResponse)
def get_menu_item_by_id(id: int, db: Session = Depends(get_db)):
    item = db.scalar(select(MenuItem).where(MenuItem.id == id))
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {id} doesn't exist"
        )

    return item

# update menu item by id


@router.patch("/{id}", response_model=MenuItemResponse)
def update_menu_item_by_id(id: int, item_update: MenuItemUpdate, db: Session = Depends(get_db)):
    item = db.scalar(select(MenuItem).where(MenuItem.id == id))

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {id} doesn't exist"
        )

    db_item = item_update.model_dump(
        exclude_unset=True
    )
    for key, value in db_item.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


# delete
@router.delete("/{id}")
def delete_menu_item_by_id(id: int, db: Session = Depends(get_db)):
    item = db.scalar(select(MenuItem).where(MenuItem.id == id))
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {id} doesn't exist"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Menu item deleted successfully"
    }

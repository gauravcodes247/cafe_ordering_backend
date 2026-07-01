from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.dependecis import get_db
router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

#Create Category

@router.post("", response_model=CategoryResponse)
def create_category( category: CategoryCreate , db: Session= Depends(get_db)):
    existing_category = db.scalar(select(Category).where(Category.name == category.name))
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail ="Category already exists"
        )
        
        
    db_category = Category(
        name = category.name,
        description =category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category
    

#Get all Category
@router.get("", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    all_categories = db.scalars(select(Category)).all()
    
    return all_categories

#get by category id
@router.get("/{id}", response_model=CategoryResponse)
def get_category_by_id(id: int, db: Session = Depends(get_db) ):
    category = db.scalar(select(Category).where(Category.id == id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} doesnt exist "
        )
    
    return category   


#update by id
@router.patch('/{id}', response_model=CategoryResponse)
def update_category_by_id(id:int, category_update:CategoryUpdate, db: Session = Depends(get_db)):
    category = db.scalar(select(Category).where(Category.id == id))
    
    if  category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} doesnt exist "
        )
        
    update_data = category_update.model_dump(
        exclude_unset=True
    )
    
    for key, value in update_data.items():
        setattr(category, key, value)    
        
    db.commit()
    db.refresh(category)

    return category    
    
#delete by id
@router.delete("/{id}")
def delete_category_by_id(id:int, db:Session = Depends(get_db)):
     category = db.scalar(select(Category).where(Category.id == id))
     if category is None:
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail=f"Category with id {id} doesnt exist "
         )
     db.delete(category)
     db.commit()
     
     return{
         'message':'Category Deleted Successfully'
     }   
      
        
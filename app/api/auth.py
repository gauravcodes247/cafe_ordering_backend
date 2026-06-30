from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import Session
from app.db.dependecis import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.models.user import User
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.email == user.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists !"
        )

    existing_username = db.scalar(
        select(User).where(User.username == user.username)
    )

    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# login api


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    stmt = select(User).where(User.email == form_data.username)
    user = db.scalar(stmt)

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

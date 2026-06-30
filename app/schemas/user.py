from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(
        min_length=8,
        max_length=200
    )
    phone: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    email: str | None = None

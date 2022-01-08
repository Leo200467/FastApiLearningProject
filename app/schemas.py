from typing import Optional
from pydantic import BaseModel, EmailStr


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: int


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserCreate(User):
    username: str

    class Config:
        orm_mode = True


class UserOutput(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(User):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        orm_mode = True

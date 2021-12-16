from typing import Optional
from pydantic import BaseModel, EmailStr

class Item(BaseModel):
    # Item class validated with Pydantic 
    name: str
    description: str
    price: float
    tax: float

class ItemResponse(Item):
    id: int

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOutput(BaseModel):
    id: int
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
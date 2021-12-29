from pydantic.networks import EmailStr
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.sql.schema import FetchedValue
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    price_with_tax = Column(Float, nullable=False, server_default='price + tax')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=FetchedValue())

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=FetchedValue())


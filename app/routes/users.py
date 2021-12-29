from fastapi.param_functions import Depends
import psycopg2
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm.session import Session
from app import models

from app.database import get_db

from .. import schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):

    user_by_id = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id:{id} not found")

    return user_by_id

from app import models, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from .. import oauth2, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)) -> dict:

    result_credentials = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not result_credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
            )

    if not utils.verify(
            user_credentials.password,
            result_credentials.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
            )

    access_token = oauth2.create_access_token(
        data={"user_id": result_credentials.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
        }

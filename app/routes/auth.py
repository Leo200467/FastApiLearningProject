from app import schemas
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import main, utils, oauth2

conn = main.conn

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends()):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * 
        FROM public.users
        WHERE email = '{credentials.username}'
        """
        )
    
    result_credentials = cursor.fetchone()

    if not result_credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
            )
    
    if not utils.verify(credentials.password, result_credentials["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
            )
    
    access_token = oauth2.create_access_token(data={"user_id": result_credentials["id"]})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }

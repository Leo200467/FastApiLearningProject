from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.jwt_secret_key

ALGORITHM = settings.jwt_algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt
    
def verify_access_token(token: str, access_exception) -> schemas.TokenData:

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")

        if id == None:
            raise access_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise access_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
                                        status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"}
                                        )

    return verify_access_token(token=token, access_exception=credential_exception)

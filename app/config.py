from pydantic import BaseSettings

class SysSettings(BaseSettings):
    database_host: str
    database_name: str
    database_user: str
    database_pwd: str 
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expiration: int

    class Config:
        env_file = ".env"

settings = SysSettings()
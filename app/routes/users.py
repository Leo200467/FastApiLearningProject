import psycopg2
from fastapi import APIRouter, HTTPException, status

from .. import main, schemas, utils

conn = main.conn

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate):
    cursor = conn.cursor()

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    try:
        cursor.execute(
            """
            INSERT INTO public.users (email, username, password) 
            VALUES (%s, %s, %s)
            RETURNING *
            """,
        (user.email, user.username, user.password)
        )
        new_user = cursor.fetchone()
        conn.commit()
    
    except psycopg2.errors.InFailedSqlTransaction:
        conn.rollback()

    cursor.close()
    return new_user

@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int):
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * FROM public.users
        WHERE id = {str(id)}
        """
        )
    result_user = cursor.fetchone()

    if not result_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} not found")
    
    cursor.close()
    return result_user
from typing import Optional

from fastapi import APIRouter, HTTPException, Response, status, Depends

from .. import main, schemas, oauth2

conn = main.conn

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@router.get("/")
def get_all_items(user_id: int = Depends(oauth2.get_current_user), limit: int = 10):

    cursor = conn.cursor()
    if limit:
        cursor.execute(
            f"""
            SELECT * 
            FROM public.items
            LIMIT {limit}
            """)
        all_items = cursor.fetchall()
        cursor.close()

        return all_items
    else:
        cursor.execute(
            """
            SELECT * 
            FROM public.items
            """)
        all_items = cursor.fetchall()
        cursor.close()

        return all_items


@router.get("/{id}", response_model=schemas.ItemResponse)
def get_item(id: int, user_id: int = Depends(oauth2.get_current_user)):
    
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * FROM public.items
        WHERE id = {str(id)}
        """
        )
    result_item = cursor.fetchone()
    if not result_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")
    cursor.close()

    return result_item

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def create_item(item: schemas.Item, user_id: int = Depends(oauth2.get_current_user)):
    
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO public.items (name, description, price, tax) 
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """,
        (item.name, item.description, item.price, item.tax)
        )
    new_item = cursor.fetchone()
    try:
        conn.commit()
        cursor.close()
        return new_item
    except ConnectionAbortedError:
        conn.rollback()

@router.delete("/{id}")
def delete_item(id: int, user_id: int = Depends(oauth2.get_current_user)):
    
    cursor = conn.cursor()
    cursor.execute(
        f"""
        DELETE FROM public.items
        WHERE id = {str(id)}
        RETURNING *
        """)
    deleted_item = cursor.fetchone()
    conn.commit()

    if deleted_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    cursor.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_item(id: int, item: schemas.Item, q: Optional[str] = None, user_id: int = Depends(oauth2.get_current_user)):
    
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE public.items
        SET name = %s, description = %s, price = %s, tax = %s
        WHERE id = %s
        RETURNING *
        """,
        (item.name, item.description, item.price, item.tax, str(id))
        )
    updated_item = cursor.fetchone()
    conn.commit()

    if updated_item == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    cursor.close()
    return updated_item

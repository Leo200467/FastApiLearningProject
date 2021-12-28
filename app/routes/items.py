from typing import Optional

from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm.session import Session
from app import models

from app.database import get_db

from .. import main, schemas, oauth2

conn = main.conn

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/sqlalchemy")
def test_sqlachemy(db: Session = Depends(get_db)):

    items = db.query(models.Items).all()
    return {"data": items}

@router.get("/")
def get_all_items(
    db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10):

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
        all_items = db.query(models.Items).all()

        return all_items

@router.get("/{id}", response_model=schemas.ItemResponse)
def get_item(id: int, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    # cursor = conn.cursor()
    # cursor.execute(
    #     f"""
    #     SELECT * FROM public.items
    #     WHERE id = {str(id)}
    #     """
    #     )
    # result_item = cursor.fetchone()
    # if not result_item:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id:{id} not found")
    # cursor.close()

    # return result_item

    item_by_id = db.query(models.Items).filter(models.Items.id == id).first()
    if not item_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    return item_by_id

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def create_item(item: schemas.Item, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    
    # cursor = conn.cursor()
    # cursor.execute(
    #     """
    #     INSERT INTO public.items (name, description, price, tax) 
    #     VALUES (%s, %s, %s, %s)
    #     RETURNING *
    #     """,
    #     (item.name, item.description, item.price, item.tax)
    #     )
    # new_item = cursor.fetchone()

    new_item = models.Items(**item.dict())

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except ConnectionAbortedError:
        db.rollback()

@router.delete("/{id}")
def delete_item(id: int, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    # cursor = conn.cursor()
    # cursor.execute(
    #     f"""
    #     DELETE FROM public.items
    #     WHERE id = {str(id)}
    #     RETURNING *
    #     """)
    # deleted_item = cursor.fetchone()
    # conn.commit()
    
    deleted_item = db.query(models.Items).filter(models.Items.id == id)

    if deleted_item.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    deleted_item.delete(synchronize_session=False)

    # cursor.close()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_item(id: int, item: schemas.Item, user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    # cursor = conn.cursor()
    # cursor.execute(
    #     """
    #     UPDATE public.items
    #     SET name = %s, description = %s, price = %s, tax = %s
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (item.name, item.description, item.price, item.tax, str(id))
    #     )
    # updated_item = cursor.fetchone()
    # conn.commit()

    updated_item_query = db.query(models.Items).filter(models.Items.id == id)

    if updated_item_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    updated_item_query.update(**item.dict(), synchronize_session=False)

    # cursor.close()
    db.commit()

    return updated_item_query.first

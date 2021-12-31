from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm.session import Session
from app import models
from typing import Optional

from app.database import get_db

from .. import schemas, oauth2

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
def get_all_items(
        db: Session = Depends(get_db), 
        user_id: int = Depends(oauth2.get_current_user),
        limit: Optional[int] = 10): 

    if limit:
        some_items = db.query(models.Items).limit(limit).all()
        return some_items
    else:
        all_items = db.query(models.Items).all()
        return all_items


@router.get("/{id}", response_model=schemas.ItemResponse)
def get_item(
        id: int, 
        user_id: int = Depends(oauth2.get_current_user), 
        db: Session = Depends(get_db)):

    item_by_id = db.query(models.Items).filter(models.Items.id == id).first()
    if not item_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    return item_by_id


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ItemResponse)
def create_item(
        item: schemas.Item, 
        db: Session = Depends(get_db), 
        user_id: int = Depends(oauth2.get_current_user)):

    new_item = models.Items(**item.dict())

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except ConnectionAbortedError:
        db.rollback()


@router.delete("/{id}")
def delete_item(
        id: int, 
        user_id: int = Depends(oauth2.get_current_user), 
        db: Session = Depends(get_db)):

    deleted_item = db.query(models.Items).filter(models.Items.id == id)

    if deleted_item.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    deleted_item.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_item(
        id: int,
        item: schemas.Item,
        user_id: int = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):

    updated_item_query = db.query(models.Items).filter(models.Items.id == id)

    updated_item_query_result = updated_item_query.first()

    if updated_item_query_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    updated_item_query.update(**item.dict(), synchronize_session=False)

    db.commit()

    return updated_item_query_result

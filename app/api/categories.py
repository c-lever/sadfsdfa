from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db import crud
from app.db.db import get_db
from app.db.schemas import CategoryInput, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryInput, db: Session = Depends(get_db)):
    return crud.create_category(db, data)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryInput,
    db: Session = Depends(get_db),
):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(db, category, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if crud.category_has_books(db, category_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Delete this category's books first",
        )
    crud.delete_category(db, category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

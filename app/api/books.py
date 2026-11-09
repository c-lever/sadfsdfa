from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db import crud
from app.db.db import get_db
from app.db.models import Category
from app.db.schemas import BookInput, BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=list[BookOut])
def list_books(category_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_books(db, category_id)

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookInput, db: Session = Depends(get_db)):
    if db.get(Category, data.category_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )
    return crud.create_book(db, data)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookInput, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db.get(Category, data.category_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )
    return crud.update_book(db, book, data)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

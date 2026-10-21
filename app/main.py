from fastapi import Depends, FastAPI, HTTPException, Response, status;
from sqlalchemy.orm import Session;
from app import crud;
from app.database import Base, Category, engine, get_db;
from app.schemas import BookInput, BookOut, CategoryInput, CategoryOut;

Base.metadata.create_all(bind=engine);
app = FastAPI(title="Book API");

@app.get("/health")
def health():
    return {"status": "ok"};

@app.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db);

@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id);
    if category is None: raise HTTPException(status_code=404, detail="Category not found");
    return category;

@app.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryInput, db: Session = Depends(get_db)):
    return crud.create_category(db, data);

@app.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryInput, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id);
    if category is None: raise HTTPException(status_code=404, detail="Category not found");
    return crud.update_category(db, category, data);

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id);
    if category is None: raise HTTPException(status_code=404, detail="Category not found");
    if crud.category_has_books(db, category_id): raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Delete this category's books first");
    crud.delete_category(db, category);
    return Response(status_code=status.HTTP_204_NO_CONTENT);

@app.get("/books", response_model=list[BookOut])
def list_books(category_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_books(db, category_id);

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id);
    if book is None: raise HTTPException(status_code=404, detail="Book not found");
    return book;

@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(data: BookInput, db: Session = Depends(get_db)):
    if db.get(Category, data.category_id) is None: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist");
    return crud.create_book(db, data);

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookInput, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id);
    if book is None: raise HTTPException(status_code=404, detail="Book not found");
    if db.get(Category, data.category_id) is None: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist");
    return crud.update_book(db, book, data);

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id);
    if book is None: raise HTTPException(status_code=404, detail="Book not found");
    crud.delete_book(db, book);
    return Response(status_code=status.HTTP_204_NO_CONTENT);

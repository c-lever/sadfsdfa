from sqlalchemy import select;
from sqlalchemy.orm import Session;
from app.database import Book, Category;
from app.schemas import BookInput, CategoryInput;

def list_categories(db: Session):
    return db.scalars(select(Category)).all();

def get_category(db: Session, category_id: int):
    return db.get(Category, category_id);

def create_category(db: Session, data: CategoryInput):
    category = Category(title=data.title);
    db.add(category);
    db.commit();
    db.refresh(category);
    return category;

def update_category(db: Session, category: Category, data: CategoryInput):
    category.title = data.title;
    db.commit();
    db.refresh(category);
    return category;

def category_has_books(db: Session, category_id: int) -> bool:
    book_id = db.scalar(select(Book.id).where(Book.category_id == category_id).limit(1));
    return book_id is not None;

def delete_category(db: Session, category: Category):
    db.delete(category);
    db.commit();

def list_books(db: Session, category_id: int | None = None):
    query = select(Book);
    if category_id is not None: query = query.where(Book.category_id == category_id);
    return db.scalars(query).all();

def get_book(db: Session, book_id: int):
    return db.get(Book, book_id);

def create_book(db: Session, data: BookInput):
    book = Book(**data.model_dump());
    db.add(book);
    db.commit();
    db.refresh(book);
    return book;

def update_book(db: Session, book: Book, data: BookInput):
    for field, value in data.model_dump().items(): setattr(book, field, value);
    db.commit();
    db.refresh(book);
    return book;

def delete_book(db: Session, book: Book):
    db.delete(book);
    db.commit();

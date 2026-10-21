from app.db.database import Base, SessionLocal, engine;
from app.db import crud;
from app.db.schemas import BookInput, CategoryInput;

def seed_database() -> None:
    Base.metadata.create_all(bind=engine);

    books_by_category = {
        "Horror": [
            ("The Shining", "A writer and his family face terror at an isolated hotel.", 12.99),
            ("Dracula", "A classic tale of Count Dracula and the people who oppose him.", 9.99),
            ("Frankenstein", "A scientist creates a living being with tragic consequences.", 10.99),
        ],
        "Fantasy": [
            ("The Hobbit", "A hobbit joins a quest to reclaim a treasure from a dragon.", 11.99),
            ("A Wizard of Earthsea", "A young wizard learns about magic, power, and responsibility.", 10.99),
            ("The Name of the Wind", "A gifted young man recounts the story of his life and studies.", 14.99),
        ],
    };

    with SessionLocal() as db:
        for category_title, books in books_by_category.items():
            category = next((item for item in crud.list_categories(db) if item.title == category_title), None);
            if category is None: category = crud.create_category(db, CategoryInput(title=category_title));
            existing_titles = { book.title for book in crud.list_books(db, category_id=category.id) };

            for title, description, price in books:
                if title not in existing_titles: crud.create_book(db, BookInput(title=title, description=description, price=price, url="", category_id=category.id));

if __name__ == "__main__":
    seed_database();
    print("Database initialized")

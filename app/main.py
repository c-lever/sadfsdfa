from app.db.database import SessionLocal;
from app.db import crud;

def main() -> None:
    with SessionLocal() as db:
        for category in crud.list_categories(db):
            print(f"\nКатегория: {category.title}");
            for book in crud.list_books(db, category_id=category.id):
                print(
                    f"  Книга: {book.title}\n"
                    f"  Описание: {book.description}\n"
                    f"  Цена: {book.price}\n"
                    f"  Ссылка: {book.url or 'не указана'}"
                );


if __name__ == "__main__":
    main();

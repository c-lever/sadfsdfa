import os;
from dotenv import load_dotenv;
from sqlalchemy import  URL, ForeignKey, String, create_engine;
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker;

load_dotenv();
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)
engine = create_engine(DATABASE_URL);
SessionLocal = sessionmaker(bind=engine);

class Base(DeclarativeBase):
    pass;

class Category(Base):
    __tablename__ = "categories";
    id: Mapped[int] = mapped_column(primary_key=True);
    title: Mapped[str] = mapped_column(String, nullable=False);

class Book(Base):
    __tablename__ = "books";
    id: Mapped[int] = mapped_column(primary_key=True);
    title: Mapped[str] = mapped_column(String, nullable=False);
    description: Mapped[str] = mapped_column(String, default="", nullable=False);
    price: Mapped[float] = mapped_column(nullable=False);
    url: Mapped[str] = mapped_column(String, default="", nullable=False);
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False);

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

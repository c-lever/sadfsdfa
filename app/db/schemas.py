from pydantic import BaseModel, ConfigDict;

class CategoryInput(BaseModel):
    title: str;

class CategoryOut(CategoryInput):
    id: int;
    model_config = ConfigDict(from_attributes=True);

class BookInput(BaseModel):
    title: str;
    description: str = "";
    price: float;
    url: str = "";
    category_id: int;

class BookOut(BookInput):
    id: int;
    model_config = ConfigDict(from_attributes=True);

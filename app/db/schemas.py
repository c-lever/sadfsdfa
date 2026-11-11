from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class CategoryInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be empty")
        return value

class CategoryOut(CategoryInput):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    url: str = ""
    category_id: int

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be empty")
        return value

class BookOut(BookInput):
    id: int
    model_config = ConfigDict(from_attributes=True)

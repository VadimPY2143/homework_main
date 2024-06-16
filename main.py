from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, ValidationError, field_validator
from typing import Any
import json
from fastapi.responses import JSONResponse

app = FastAPI()


class Item(BaseModel):
    title: str
    author: str
    year: int
    isbn: str

    @field_validator('title')
    @classmethod
    def title_check(cls, value: Any):
        if len(value) == 0:
            raise ValueError("Це поле є обов'язкове")
        return value

    @field_validator('author')
    @classmethod
    def author_check(cls, value: Any):
        if len(value) == 0:
            raise ValueError("Це поле є обов'язкове")
        return value

    @field_validator('year')
    @classmethod
    def year_check(cls, value: Any):
        if value >= 1500 and value <= 2024:
            return value
        raise ValueError("Неправильний рік")


    @field_validator('isbn')
    @classmethod
    def isbn_check(cls, value: Any):
        if len(value) == 13 or len(value) == 0:
            return value
        else:
            raise ValueError("Неправильна інформація")


books_base = []

@app.post("/books/")
def create_item(item: Item):
    books_base.append(item.model_dump_json())
    return JSONResponse(content=item.model_dump_json(), status_code=201)
@app.get('/books/')
def get_books():
    return books_base



if __name__ == "__main__":
    uvicorn.run(app)
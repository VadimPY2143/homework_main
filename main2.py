from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, ValidationError, field_validator, EmailStr
from typing import Any, Union
import json
from fastapi.responses import JSONResponse


app = FastAPI()


users = []
addresses = []
class User(BaseModel):
    id: int
    name: str
    age: int = None
    email: EmailStr

    @field_validator('name')
    @classmethod
    def check_name(cls, value: Any):
        if len(value) == 0:
            raise ValueError("Це поле є обов'язкове")
        return value

    @field_validator('email')
    @classmethod
    def check_email(cls, value: Any):
        if len(value) == 0:
            raise ValueError("Це поле є обов'язкове")
        return value


class Address(BaseModel):
    user_id: int
    address: str
    type: Union[str, None]



@app.post('/users/')
def add_user(user: User):
    users.append(user.dict())
    return JSONResponse(status_code= 201, content=user.dict())


@app.get('/users/')
def get_users():
    return users


@app.post('/addresses/')
def add_address(address: Address):
    addresses.append(address.dict())
    return JSONResponse(status_code= 201, content=address.dict())


@app.get('/addresses/')
def get_addresses():
    return addresses




if __name__ == "__main__":
    uvicorn.run(app)
from datetime import datetime
# from typing import Optional
from pydantic import Field
import uuid
import requests
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body, Path, Query
app = FastAPI()

# Models


class Dog(BaseModel):
    id: str = Field(default=uuid.uuid4())
    name: str = Field(..., min_length=1, max_length=50)
    picture: str = Field(default=requests.get(
        "https://dog.ceo/api/breeds/image/random").json()["message"])
    is_adopted: bool
    create_date: datetime = None

    class Config:
        schema_extra = {
            "example":
            {
                "name": "Tito",
                "picture": "https://images.dog.ceo/breeds/mastiff-english/2.jpg",
                "is_adopted": False,
                "create_date": "2021, 10, 25, 22, 56, 15, 858589"
            }
        }


# Path operation definitions with path parameters and query parameters.

# Request and Response Body


@app.get("/")
async def home():
    return {"message": "Ok"}


@app.get("/api/dogs")
async def dogs():
    return {"message": "list dogs"}


@app.get("/api/dogs/{dog_name}")
async def show_dog(dog_name: str = Path(
        ...,
        min_length=1,
        max_length=20,
        title="Dog Name",)):
    return {"dog_name": dog_name}


@app.get("/api/dogs")
async def is_adopted(
    is_adopted: bool = Query(True)
):
    return {"dog_name": None}


@app.post("/api/dogs/new")
async def create_dog(dog: Dog = Body(...)):
    return dog


@app.put("/api/dogs/{name}")
async def update_dog(
    name: str = Path(
        ...,
    ),
    dog: Dog = Body(...)
):
    return dog

from datetime import datetime
from pydantic import Field
import uuid
from pydantic.networks import EmailStr
import requests
from pydantic import BaseModel, UUID4
from fastapi import FastAPI

from routes.user import user
from fastapi import (Body, Path, Query)

app = FastAPI(title="Guane-Intern-FastAPI",
              description="REST API builded using FastAPI framework and MondoDB as database.")
app.include_router(user)


# Models


class Dog(BaseModel):
    id: str = Field(default=uuid.uuid4())
    name: str = Field(..., min_length=1, max_length=50)
    picture: str = Field(default=requests.get(
        "https://dog.ceo/api/breeds/image/random").json()["message"])
    is_adopted: bool
    create_date: datetime = None
    id_user: UUID4


# Path operation definitions with path parameters and query parameters.

# Request and Response Body


@app.get("/")
async def home():
    # db['dogs']=
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
    db['dogs'].insert_one(dog)
    return dog


@app.put("/api/dogs/{name}")
async def update_dog(
    name: str = Path(
        ...,
    ),
    dog: Dog = Body(...)
):
    return dog

# User CRUD

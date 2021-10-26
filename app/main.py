from datetime import datetime
# from typing import Optional
from pydantic.fields import Field
import uuid
import requests
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

# Models


class Dog(BaseModel):
    id: str = Field(default=uuid.uuid4())
    name: str
    picture: str = Field(default=requests.get(
        "https://dog.ceo/api/breeds/image/random").json()["message"])
    is_adopted: bool
    create_date: datetime = None


# Path operation definitions with path parameters and query parameters.

# Request and Response Body


@app.get("/")
async def home():
    return {"message": "Ok"}


@app.get("/api/dogs")
async def dogs():
    return {"message": "list dogs"}


@app.get("/api/dogs/{dog_name}")
async def show_dog(dog_name: str):
    return {"dog_name": dog_name}


@app.get("/api/dogs?is_adopted=True")
async def is_adopted():
    return {"dog_name": None}


@app.post("/api/dogs/new")
async def create_dog(dog: Dog = Body(...)):
    return dog

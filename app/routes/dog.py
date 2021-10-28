from fastapi import APIRouter, Response
from fastapi.param_functions import Query
from models.dog import Dog
from schemas.dog import dogsEntity, dogEntity
from config.db import client
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT


dog = APIRouter()


@dog.get("/api/dogs")
async def get_dogs():
    dogs = client.guane_db.dogs.find()
    return dogsEntity(dogs)


@dog.post("/api/dogs/")
async def create_dog(dog: Dog):
    new_dog = dict(dog)
    id_dog = client.guane_db.dogs.insert_one(new_dog).inserted_id
    new_dog = client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)})
    return dogEntity(new_dog)


@dog.get("/api/dogs/{id_dog}")
async def show_dog(id_dog: str):
    return dogEntity(client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)}))


@dog.get("/api/dogs/")
async def is_adopted(is_adopted: bool = Query(...)):
    dogs = client.guane_db.dogs.find({"is_adopted":is_adopted})
    return dogsEntity(dogs)

@dog.delete("/api/dogs/{id_dog}")
async def delete_dog(id_dog):
    dogEntity(client.guane_db.dogs.find_one_and_delete(
        {"_id": ObjectId(id_dog)}))
    return Response(status_code=HTTP_204_NO_CONTENT)


@dog.put("/api/dogs/{id_dog}/")
async def update_dog(id_dog: str, dog: Dog):
    client.guane_db.dogs.find_one_and_update(
        {"_id": ObjectId(id_dog)}, {"$set": dict(dog)})
    return dogEntity(client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)}))

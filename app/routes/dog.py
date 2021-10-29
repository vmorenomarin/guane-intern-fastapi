from fastapi import APIRouter, Depends
from fastapi.param_functions import Query
from models.dog import Dog
from schemas.dog import dogsEntity, dogEntity
from config.db import client
from bson import ObjectId
from controllers.login import get_current_active_user

dog = APIRouter()


@dog.get("/api/dogs", tags=["Dogs"])
async def get_dogs():
    dogs = client.guane_db.dogs.find()
    return dogsEntity(dogs)


@dog.post("/api/dogs/", tags=["Dogs"])
async def create_dog(dog: Dog = Depends(get_current_active_user)):
    new_dog = dict(dog)
    id_dog = client.guane_db.dogs.insert_one(new_dog).inserted_id
    new_dog = client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)})
    return dogEntity(new_dog)


@dog.get("/api/dogs/{id_dog}", tags=["Dogs"])
async def show_dog(id_dog: str):
    return dogEntity(client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)}))


@dog.get("/api/dogs/", tags=["Dogs"])
async def is_adopted(is_adopted: bool = Query(...)):
    dogs = client.guane_db.dogs.find({"is_adopted": is_adopted})
    return dogsEntity(dogs)


@dog.get("/api/dogs/user/", tags=["Dogs"])
async def get_dogs_by_user(user_id: str = Query(...)):
    dogs = client.guane_db.dogs.find({"user_id": user_id})
    return dogsEntity(dogs)
    

@dog.delete("/api/dogs/{id_dog}", tags=["Dogs"])
async def delete_dog(id_dog):
    dogEntity(client.guane_db.dogs.find_one_and_delete(
        {"_id": ObjectId(id_dog)}))
    return {"id_deleted": id_dog,
            "message": "Dog deleted."}


@dog.put("/api/dogs/{id_dog}/", tags=["Dogs"])
async def update_dog(id_dog: str, dog: Dog):
    client.guane_db.dogs.find_one_and_update(
        {"_id": ObjectId(id_dog)}, {"$set": dict(dog)})
    return dogEntity(client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)}))

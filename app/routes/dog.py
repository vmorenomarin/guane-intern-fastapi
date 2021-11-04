"""
This script defines the path operations for dog endpoint.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# Python libraries
from bson import ObjectId

# FastAPI libraries
from fastapi import APIRouter, Depends
from fastapi.param_functions import Query

# App functions, models and routes
from models.dog import Dog
from schemas.dog import dogsEntity, dogEntity
from config.db import client
from controllers.login import get_current_active_user

# APIRouter instance
dog = APIRouter()


# Request dogs
@dog.get("/api/dogs", tags=["Dogs"])
async def get_dogs():
    """
    Get dogs.

    This function allow get all dogs in database.

    Returns a list of all dogs in database.
    """
    dogs = client.guane_db.dogs.find()
    return dogsEntity(dogs)


# Post a new user
@dog.post("/api/dogs/", tags=["Dogs"])
async def create_dog(dog: Dog = Depends(get_current_active_user)):
    """
    Create dog.

    This function allow create a dog for previously authenticated users.

    Parameters:
        - dog: Dog -> Dog based in Dog model.

    Returns data for a new dog in database.
    """
    new_dog = dict(dog)
    id_dog = client.guane_db.dogs.insert_one(new_dog).inserted_id
    new_dog = client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)})
    return dogEntity(new_dog)


# Get dog by ID
@dog.get("/api/dogs/{id_dog}", tags=["Dogs"])
async def show_dog(id_dog: str):
    """
    Show dog by ID.

    This function allow retrieve info of a dog by its id.

    Parameters:
        - id_dog: str -> Dog ID to locate in database.

    Returns data for a query dog.
    """
    return dogEntity(client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)}))


# Get adopted dogs
@dog.get("/api/dogs/", tags=["Dogs"])
async def is_adopted(is_adopted: bool = Query(...)):
    """
    Show if dog(s) is/are adopted.

    This function return a list of  adopted dogs if query parameter is true.

    Parameters:
        - id_adopted: bool -> True is need see adopted dogs.

    Returns list of adopted dogs.
    """
    dogs = client.guane_db.dogs.find({"is_adopted": is_adopted})
    return dogsEntity(dogs)


# Get dogs with same owner
@dog.get("/api/dogs/user/", tags=["Dogs"])
async def get_dogs_by_user(user_id: str = Query(...)):
    """
    Show all dogs from a user.

    This function return a list of dogs for a particular user.

    Parameters:
        - user_id: str -> User id to see own dogs.

    Returns list of dogs with same user id owner.
    """
    dogs = client.guane_db.dogs.find({"user_id": user_id})
    return dogsEntity(dogs)


# Delete dog
@dog.delete("/api/dogs/{id_dog}", tags=["Dogs"])
async def delete_dog(id_dog):
    """
    Delete dog by ID.

    This function allow delete a dog by id.

    Parameters:
        - id_dog: str -> Dog ID to locate in database.

    Returns dict with deleted dog id and info message.
    """
    dogEntity(client.guane_db.dogs.find_one_and_delete(
        {"_id": ObjectId(id_dog)}))
    return {"id_deleted": id_dog,
            "message": "Dog deleted."}


# Update dog data
@dog.put("/api/dogs/{id_dog}/", tags=["Dogs"])
async def update_dog(id_dog: str, dog: Dog):
    """
    Update dog data.

    This function allow update dog data by id.

    Parameters:
        - id_dog: str -> Dog ID to locate in database.
        - dog: Dog -> Dog data to update.

    Returns updated dog data.
    """
    client.guane_db.dogs.find_one_and_update(
        {"_id": ObjectId(id_dog)}, {"$set": dict(dog)})
    return dogEntity(client.guane_db.dogs.find_one({"_id": ObjectId(id_dog)}))

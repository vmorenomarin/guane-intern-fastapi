"""
This script defines the path operations for user endpoint.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# Python libraries
from bson import ObjectId

# FastAPI libraries
from fastapi import APIRouter, Depends

# App functions, models and routes
from schemas.user import usersEntity, userEntity
from models.user import User
from config.db import client
from controllers.login import get_current_active_user

# APIRouter instance
user = APIRouter()


# Request users
@user.get("/api/users", tags=["Users"])
async def get_users():
    """
    Get users.

    This function allow get all users in database.

    Returns a list of all users in database.
    """
    users = client.guane_db.users.find()
    return usersEntity(users)


# Post a new user
@user.post("/api/users", tags=["Users"])
async def create_user(user: User = Depends(get_current_active_user)):
    """
    Create user.

    This function allow create a user for previously authenticated users.

    Parameters:
        - user: User -> User based in User model.

    Returns data for a new user in database.
    """
    new_user = dict(user)
    id_user = client.guane_db.users.insert_one(new_user).inserted_id
    new_user = client.guane_db.users.find_one({"_id": ObjectId(id_user)})
    return userEntity(new_user)


# Get user by ID
@user.get("/api/users/{id_user}", tags=["Users"])
async def show_user(id_user: str):
    """
    Show user by ID.

    This function allow retrieve info of a user by the id.

    Parameters:
        - id_user: str -> User ID to locate in database.

    Returns data for a query user.
    """
    return userEntity(
        client.guane_db.users.find_one({"_id": ObjectId(id_user)}))


# Delete user
@user.delete("/api/users/{id_user}", tags=["Users"])
async def delete_user(id_user):
    """
    Delete user by ID.

    This function allow delete a user by id.

    Parameters:
        - id_user: str -> User ID to locate in database.

    Returns dict with deleted user id and info message.
    """
    userEntity(client.guane_db.users.find_one_and_delete(
        {"_id": ObjectId(id_user)}))
    return {"id_deleted": id_user,
            "message": "User deleted."}


# Update user data
@user.put("/api/users/{id_user}", tags=["Users"])
async def update_user(id_user: str, user: User):
    """
    Update user data.

    This function allow update user data by id.

    Parameters:
        - id_user: str -> User ID to locate in database.
        - user: User -> User data to update.

    Returns updated user data.
    """
    client.guane_db.users.find_one_and_update(
        {"_id": ObjectId(id_user)}, {"$set": dict(user)})
    return userEntity(
        client.guane_db.users.find_one({"_id": ObjectId(id_user)}))

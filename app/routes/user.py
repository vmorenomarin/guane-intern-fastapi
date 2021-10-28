from fastapi import APIRouter
from models.user import User
from schemas.user import usersEntity, userEntity
from config.db import client
from bson import ObjectId


user = APIRouter()


@user.get("/api/users")
async def get_users():
    users = client.guane_db.users.find()
    return usersEntity(users)


@user.post("/api/users/")
async def create_user(user: User):
    new_user = dict(user)
    id_user = client.guane_db.users.insert_one(new_user).inserted_id
    new_user = client.guane_db.users.find_one({"_id": ObjectId(id_user)})
    return userEntity(new_user)


@user.get("/api/users/{id_user}")
async def show_user(id_user: str):
    return userEntity(client.guane_db.users.find_one({"_id": ObjectId(id_user)}))


@user.delete("/api/users/{id_user}")
async def delete_user(id_user):
    userEntity(client.guane_db.users.find_one_and_delete(
        {"_id": ObjectId(id_user)}))
    return {"id_deleted": id_user,
            "message": "User deleted."}


@user.put("/api/users/{id_user}/")
async def update_user(id_user: str, user: User):
    client.guane_db.users.find_one_and_update(
        {"_id": ObjectId(id_user)}, {"$set": dict(user)})
    return userEntity(client.guane_db.users.find_one({"_id": ObjectId(id_user)}))
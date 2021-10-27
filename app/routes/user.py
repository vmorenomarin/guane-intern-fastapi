from fastapi import APIRouter, Response, status
from fastapi import Body, Path, Query
from models.user import User
from schemas.user import usersEntity, userEntity
from config.db import client
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT


user = APIRouter()


@user.get("/api/users")
async def get_users():
    return usersEntity(client.guane_db.users.find())


@user.post("/api/users/")
async def create_user(user: User):
    new_user = dict(user)
    id_user = client.guane_db.users.insert_one(new_user).inserted_id
    user = client.guane_db.users.find_one({"_id": ObjectId(id_user)})
    return userEntity(user)


@user.get("/api/users/{id_user}")
async def show_user(id_user: str):
    return userEntity(client.guane_db.users.find_one({"_id": ObjectId(id_user)}))


@user.delete("/api/users/{id_user}")
async def delete_user(id_user):
    userEntity(client.guane_db.users.find_one_and_delete(
        {"_id": ObjectId(id_user)}))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/api/users/{id_user}/")
async def update_user(id_user: str, user: User):
    client.guane_db.users.find_one_and_update({"_id": ObjectId(id_user)},{"$set":dict(user)})
   
    return userEntity(client.guane_db.users.find_one({"_id": ObjectId(id_user)}))

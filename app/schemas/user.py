def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "username":item["username"],
        "name": item["name"],
        "lastname": item["lastname"],
        "email": item["email"],
        "hashed_password": item["password"]
    }

def usersEntity(users) -> list:
    return [userEntity(item) for item in users]
    
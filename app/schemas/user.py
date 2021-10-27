def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "lastname": item["lastname"],
        "email": item["email"]
    }

def usersEntity(users) -> list:
    return [userEntity(item) for item in users]
    
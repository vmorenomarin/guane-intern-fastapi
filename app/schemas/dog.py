def dogEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "picture": item["picture"],
        "is_adopted": item["is_adopted"],
        "created_date": item["created_date"],
        "user_id": item["user_id"]
    }

def dogsEntity(dogs) -> list:
    return [dogEntity(item) for item in dogs]
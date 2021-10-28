def dogEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "picture": item["picture"],
        "is_adopted": item["is_adopted"],
        "create_date": item["create_date"],
        "user_id": item["user_id"]
    }

def dogsEntity(dogs) -> list:
    return [dogEntity(item) for item in dogs]
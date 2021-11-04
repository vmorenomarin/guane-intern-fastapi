"""
Defines dog entities to build dictionary with dog and a list with dogs data.

Author: Victor Moreno Marin
Date: 03/11/2021
"""


def dogEntity(item) -> dict:
    """
    Dog entity.

    Build a dictionary with dog data scheme.

    Paramaters:
        - item -> Dog model object

    Returns dictionary with Dog data.
    """
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "picture": item["picture"],
        "is_adopted": item["is_adopted"],
        "create_date": item["create_date"],
        "user_id": item["user_id"]
    }


def dogsEntity(dogs) -> list:
    """
    Dogs entity.

    Build a list with dogs data.

    Paramaters:
        - dogs -> Dogs list from database.

    Returns list with dogs with dog entity data scheme.
    """
    return [dogEntity(item) for item in dogs]

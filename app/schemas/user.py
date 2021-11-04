"""
Defines user entities to build dictionary with user and a list with users data.

Author: Victor Moreno Marin
Date: 03/11/2021
"""


def userEntity(item) -> dict:
    """
    User entity.

    Build a dictionary with user data scheme.

    Paramaters:
        - item -> User model object

    Returns dictionary with user data.
    """
    return {
        "id": str(item["_id"]),
        "username": item["username"],
        "name": item["name"],
        "lastname": item["lastname"],
        "email": item["email"],
        "hashed_password": item["password"]
    }


def usersEntity(users) -> list:
    """
    Users entity.

    Build a list with users data.

    Paramaters:
        - users -> Users list from database.

    Returns list with users with user entity data scheme.
    """
    return [userEntity(item) for item in users]

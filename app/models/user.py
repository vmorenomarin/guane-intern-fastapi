"""
Build a user class.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# FastAPI and Pydantic libraries
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    User model.

    Build an user class.
    """

    username: str
    name: str
    lastname: str
    email: str
    hashed_password: Optional[str] = None

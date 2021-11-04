"""
This script build classes necessary to user authentication.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# Python libraries
from typing import Optional

# Pydantic libraries
from pydantic import BaseModel

# User model
from models.user import User


class Token(BaseModel):
    """
    Token model.

    Build a Token class.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token data model.

    Build a Token data class.
    """

    username: Optional[str] = None


class UserInDB(User):
    """
    User in database.

    Inherits User model properties and add hashed password
    if user exists in database.
    """

    hashed_password: str

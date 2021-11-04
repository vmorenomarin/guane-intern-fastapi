"""
Build a dog class.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# Python libraries
import requests
from datetime import datetime

# Pydantic libraries
from pydantic import BaseModel, Field


class Dog(BaseModel):
    """
    Dog model.

    Build a dog class.
    """

    name: str
    picture: str = Field(default=requests.get(
        "https://dog.ceo/api/breeds/image/random").json()["message"])
    is_adopted: bool
    create_date: datetime = None
    user_id: str

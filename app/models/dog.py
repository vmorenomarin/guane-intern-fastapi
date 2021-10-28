from pydantic import BaseModel, Field
from datetime import datetime
import requests

class Dog(BaseModel):
    name: str
    picture: str = Field(default=requests.get(
        "https://dog.ceo/api/breeds/image/random").json()["message"])
    is_adopted: bool
    create_date: datetime = None
    id_user: str
    

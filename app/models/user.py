from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    name: str
    lastname: str
    email: str
    hashed_password: Optional[str] = None

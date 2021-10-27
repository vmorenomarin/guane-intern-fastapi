from pydantic.networks import EmailStr
from pydantic import (BaseModel, UUID4, Field)

class User(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)
    lastname: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(...)
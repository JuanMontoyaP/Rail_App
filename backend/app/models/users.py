from re import U
from typing import Optional
from bson import ObjectId
from enum import Enum

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

from .id import PyObjectId


class Role(Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    role: Optional[Role] = Field(default="user")

    class Config:
        json_encoders = {ObjectId: str}
        orm_mode = True


class UserEmail(User):
    email: EmailStr = Field(...)


class UserPassword(UserEmail):
    password: str = Field(
        ...,
        min_length=8,
    )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Pink",
                "last_name": "Floyd",
                "email": "pinkFloyd@pk.com",
                "password": "Pink123456789"}
        }

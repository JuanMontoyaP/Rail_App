from msilib import schema
from tkinter import E
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
    fist_name: str = Field(
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


class UserPassword(User):
    email: EmailStr = Field(...)
    password: str = Field(
        ...,
        min_length=8,
    )

    class Config:
        schema_extra = {
            "example": {
                "fist_name": "Pink",
                "last_name": "Floyd",
                "email": "pinkFloyd@pk.com",
                "password": "Pink123456789"}
        }

from fastapi import APIRouter
from fastapi import Body

from fastapi import status

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..models import users
from ..database.client import connect_to_database

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(path="/")
async def get_users():
    return [{"user": "rail"}]


@router.post(
    path="/",
    response_description="Create a new user",
    response_model=users.User)
async def create_user(user: users.UserPassword = Body(...)):
    """
    create_user

    This path operation creates a new user in the database.

    Parameters:

        - Request body parameter:

            - **user: UserPassword** -> A user model with first name, last_name, email and password.

    Returns a json with the basic user information:

        - _id: PyObjectId
        - email: EmailStr
        - firs_name: str
        - last_name: str
        - role: Enum
    """
    user = jsonable_encoder(user)

    db = connect_to_database("rail")
    new_user = await db["users"].insert_one(user)
    create_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_user)


@router.put(path="/")
async def update_user(username: str, password: str):
    pass


@router.delete(path="/")
async def delete_user(username: str):
    pass

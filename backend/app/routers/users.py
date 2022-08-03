from fastapi import APIRouter
from fastapi import Body
from fastapi import status, HTTPException

from fastapi.responses import JSONResponse

from ..models import users
from ..services.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_service = UserService()


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
    try:
        create_user = await user_service.create_new_user(user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_user)
    except Exception as error:
        msg = error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(msg)
        )


@router.put(path="/")
async def update_user(username: str, password: str):
    pass


@router.delete(path="/")
async def delete_user(username: str):
    pass

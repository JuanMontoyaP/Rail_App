from pydantic import EmailStr

from fastapi import APIRouter
from fastapi import Path, Body
from fastapi import status, HTTPException

from ..models import users, id
from ..services.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_service = UserService()


@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=users.UserEmail,
    summary="Get the user information by ID"
)
async def get_user(
    user_id: id.PyObjectId = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        example="62eac89c25d89e25b79a06f1"
    )
):
    """
    get_user

    Get a specific user by ID from the database.

    Parameters:

        - Request path parameter:

            - **user_id: PyObjectId** -> The user ID.

    Returns a json with the basic user information:

        - _id: PyObjectId
        - email: EmailStr
        - firs_name: str
        - last_name: str
        - role: Enum
    """
    try:
        user = await user_service.get_a_user(user_id)
        return user
    except Exception as error:
        msg = error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(msg)
        )


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=users.User,
    response_description="User created successfully",
    summary="Create a new user"
)
async def create_user(
    user: users.UserPassword = Body(...)
):
    """
    create_user

    This path operation creates a new user in the database.

    Parameters:

        - Request body parameter:

            - **user: UserPassword** -> A user model with first name, last_name, email and password.

    Returns a json with the created user information:

        - _id: PyObjectId
        - email: EmailStr
        - firs_name: str
        - last_name: str
        - role: Enum
    """
    try:
        create_user = await user_service.create_new_user(user)
        return create_user
    except Exception as error:
        msg = error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(msg)
        )


@router.put(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=users.UserEmail,
    response_description="User updated successfully",
    summary="Update a user"
)
async def update_user(
    user_id: id.PyObjectId = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        example="62eac89c25d89e25b79a06f1"
    ),
    update_user: users.UserPassword = Body(...)
):
    pass


@ router.delete(path="/")
async def delete_user(username: str):
    pass

from fastapi.encoders import jsonable_encoder

from ..database.client import connect_to_database
from ..models import users


class UserService:
    def __init__(self):
        self.db = connect_to_database("rail")

    async def create_new_user(self, user: users.UserPassword) -> users.UserPassword:
        """
        It takes a user object, encodes it to JSON, inserts it into the database, and then returns the
        newly created user object

        Args:
          user (users.UserPassword): users.UserPassword

        Returns:
          The user object that was created.
        """
        user = jsonable_encoder(user)
        new_user = await self.db["users"].insert_one(user)
        created_user = await self.db["users"].find_one({"_id": new_user.inserted_id})
        return created_user

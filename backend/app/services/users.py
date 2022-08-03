from hashlib import new
import bcrypt

from fastapi.encoders import jsonable_encoder

from ..database.client import connect_to_database
from ..models import users, id
from ..utils.validators import db_validators


class UserService:
    def __init__(self):
        self.client = connect_to_database()
        self.db = self.client["users"]

    def __hash_password(self, password):
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(6))
        return hashed_password

    async def get_a_user(self, user_id: id.PyObjectId):
        """
        It takes a user_id, finds the user in the database, and returns the user

        Args:
          user_id (id.PyObjectId): id.PyObjectId

        Returns:
          A user object
        """
        user = await self.db.find_one({"_id": str(user_id)})
        if not user:
            raise Exception("User not found")

        return user

    async def create_new_user(self, user: users.UserPassword) -> users.UserPassword:
        """
        It takes a user object, encodes it to JSON, inserts it into the database, and then returns the
        newly created user object

        Args:
          user (users.UserPassword): users.UserPassword

        Returns:
          The user object that was created.
        """
        email_validator = await db_validators.validate_unique_email(user.email)

        if email_validator:
            raise Exception("The user already exists")

        user.password = self.__hash_password(user.password)

        user = jsonable_encoder(user)
        new_user = await self.db.insert_one(user)
        created_user = await self.db.find_one({"_id": new_user.inserted_id})
        return created_user

    async def update_user_info(self, user_id: id.ObjectId, new_info: users.UserPassword) -> users.UserPassword:
        """
        It updates a user's information in the database

        Args:
          user_id (id.ObjectId): id.ObjectId
          new_info (users.UserPassword): users.UserPassword

        Returns:
          The updated user
        """

        email_validator = await db_validators.validate_unique_email(new_info.email)

        if email_validator:
            raise Exception("The email already exists")

        await self.db.update_one(
            {"_id": str(user_id)},
            {'$set': {
                "first_name": new_info.first_name,
                "last_name": new_info.last_name,
                "email": new_info.email,
                "password": self.__hash_password(new_info.password)
            }
            }
        )

        updated_user = await self.get_a_user(user_id)

        return updated_user

    async def delete_a_user(self, user_id):
        pass

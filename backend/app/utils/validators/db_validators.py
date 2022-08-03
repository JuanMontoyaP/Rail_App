from pydantic import EmailStr

from ...database import client

db = client.connect_to_database()


async def validate_unique_email(email: EmailStr, collection: str = "users"):
    exited_user = await db[collection].find_one({"email": email})
    return exited_user

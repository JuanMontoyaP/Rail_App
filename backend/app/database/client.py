import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()


def connect_to_database(database_name: str):
    client = motor.motor_asyncio.AsyncIOMotorClient(
        os.environ["MONGODB_URL"])

    return client[database_name]

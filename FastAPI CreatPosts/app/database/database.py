# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"  

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.posts_db
collection = database.get_collection("posts_collection")

async def create_database():
    print("MongoDB подключена:", MONGO_DETAILS)
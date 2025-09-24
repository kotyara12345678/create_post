# test_mongo.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

MONGO_DETAILS = "mongodb://mongo:27017"  # Адрес твоего MongoDB

# JSON поста
post_data = {
    "title": "Тестовый пост",
    "content": "Это тестовый контент для проверки",
    "link": "https://example.com",
    "price": 100,
    "media": ["https://example.com/media.png"],
    "show_link": False,
    "published": datetime.utcnow()
}

async def main():
    client = AsyncIOMotorClient(MONGO_DETAILS)
    db = client.posts_db
    collection = db.posts_collection

    # Проверка подключения
    try:
        await client.admin.command("ping")
        print("✅ MongoDB подключена!")
    except Exception as e:
        print("❌ Ошибка подключения к MongoDB:", e)
        return

    # Вставка поста
    try:
        result = await collection.insert_one(post_data)
        print("✅ Пост вставлен с ID:", result.inserted_id)

        # Получаем пост обратно
        post = await collection.find_one({"_id": result.inserted_id})
        print("📄 Полученный пост:")
        print(post)
    except Exception as e:
        print("❌ Ошибка при работе с коллекцией:", e)

if __name__ == "__main__":
    asyncio.run(main())
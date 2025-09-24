from fastapi import APIRouter, HTTPException
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import base64

from .database import collection
from .models import PostCreate
from .schemas import ActivityStreamsCreate, ActivityStreamsNote
from pydantic import Field

router = APIRouter()

def post_to_activity(post, paid: bool = False) -> dict:
    # Если платная ссылка и ещё не оплачено — контент в base64
    content = post["content"]
    if post.get("show_link", False) and not paid:
        content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    note = ActivityStreamsNote(
        id=str(post["_id"]),
        title=post["title"],
        content=content,
        link=post.get("link"),
        price=post["price"],
        media=[str(m) for m in post.get("media", [])],
        show_link=post.get("show_link", False),
        published=post.get("published", datetime.utcnow())
    )

    activity = ActivityStreamsCreate(
        **{
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Create",
            "id": f"https://example.com/posts/{note.id}",
            "actor": "https://example.com/@username",
            "object": note,
            "published": note.published
        }
    )
    return activity.model_dump(by_alias=True)  # важно для @context

# Создать новый пост
@router.post("/posts", response_model=ActivityStreamsCreate)
async def create_post(post: PostCreate):
    # Преобразуем Pydantic объект в словарь и конвертируем HttpUrl в строки
    post_dict = post.dict()
    
    # Конвертируем HttpUrl объекты в строки для MongoDB
    if post_dict.get("link"):
        post_dict["link"] = str(post_dict["link"])
    
    if post_dict.get("media"):
        post_dict["media"] = [str(url) for url in post_dict["media"]]
    
    post_dict["show_link"] = post_dict.get("show_link", False)
    post_dict["published"] = datetime.utcnow()
    
    result = await collection.insert_one(post_dict)
    new_post = await collection.find_one({"_id": result.inserted_id})
    return post_to_activity(new_post)

# Получить все посты
@router.get("/getposts", response_model=List[ActivityStreamsCreate])
async def get_posts():
    posts = []
    async for post in collection.find():
        posts.append(post_to_activity(post))
    return posts

# Получить пост по ID
@router.get("/posts/{post_id}", response_model=ActivityStreamsCreate)
async def get_post(post_id: str):
    try:
        post = await collection.find_one({"_id": ObjectId(post_id)})
        if post:
            return post_to_activity(post)
        raise HTTPException(status_code=404, detail="Post not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid post ID")

# Оплата поста
@router.post("/posts/{post_id}/pay", response_model=ActivityStreamsCreate)
async def pay_post(post_id: str):
    try:
        post = await collection.find_one({"_id": ObjectId(post_id)})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post_to_activity(post, paid=True)
    except:
        raise HTTPException(status_code=400, detail="Invalid post ID")

@router.put("/posts/{post_id}", response_model=ActivityStreamsCreate)
async def update_post(post_id: str, post: PostCreate):
    try:
        # Преобразуем обновленные данные для MongoDB
        update_data = post.dict()
        
        # Конвертируем HttpUrl объекты в строки
        if update_data.get("link"):
            update_data["link"] = str(update_data["link"])
        
        if update_data.get("media"):
            update_data["media"] = [str(url) for url in update_data["media"]]
        
        result = await collection.update_one(
            {"_id": ObjectId(post_id)}, 
            {"$set": update_data}
        )
        if result.modified_count:
            updated = await collection.find_one({"_id": ObjectId(post_id)})
            return post_to_activity(updated)
        raise HTTPException(status_code=404, detail="Post not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid post ID")

# Удалить пост
@router.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    try:
        result = await collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count:
            return {"status": "deleted"}
        raise HTTPException(status_code=404, detail="Post not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid post ID")
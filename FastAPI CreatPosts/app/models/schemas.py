from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class ActivityStreamsNote(BaseModel):
    id: str
    title: str
    content: str
    link: Optional[HttpUrl]
    price: float
    media: List[HttpUrl] = []
    show_link: bool = False
    published: datetime

class ActivityStreamsCreate(BaseModel):
    context: str = Field(..., alias='@context')  # обязательно через alias
    type: str = "Create"
    id: str  # uuid или URL поста
    actor: str  # вроде https://example.com/@username
    object: ActivityStreamsNote
    published: datetime

    class Config:
        populate_by_name = True
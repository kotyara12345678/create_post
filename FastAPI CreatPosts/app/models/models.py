from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List


class PostCreate(BaseModel):
    title: str = Field(..., description="Название поста")
    content: str = Field(..., description="Основной текст поста", min_length=10)
    link: Optional[HttpUrl] = Field(None, description="Ссылка на внешний ресурс")
    price: float = Field(..., description="Стоимость", ge=0)
    media: Optional[List[HttpUrl]] = Field(None, description="Список медиа файлов")
    show_link: Optional[bool] = Field(False, description="Контент платный")  # новый флаг


class PostResponse(PostCreate):
    id: str = Field(..., description="ID записи в базе")
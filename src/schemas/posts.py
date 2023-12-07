from pydantic import BaseModel
from datetime import datetime


class CreatePost(BaseModel):
    title: str
    desc: str
    img: str
    sold: bool = False
    created_at: datetime = datetime.now()
    price: int


class IdentifyPost(BaseModel):
    post_id: int

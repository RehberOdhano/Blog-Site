from pydantic import BaseModel

from schemas.user import ShowUserSchema


class BlogSchema(BaseModel):
    title: str
    body: str
    user_id: int


class ShowBlogSchema(BaseModel):
    title: str
    body: str
    author: ShowUserSchema

    class Config:
        orm_mode = True

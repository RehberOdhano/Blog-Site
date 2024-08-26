from typing import List

from pydantic import BaseModel


class UserBlogSchema(BaseModel):
    title: str
    body: str


class ShowUserSchema(BaseModel):
    name: str
    email: str
    blogs: List[UserBlogSchema] = []

    class Config:
        orm_mode = True

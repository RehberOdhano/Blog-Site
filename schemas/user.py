from typing import List

from pydantic import BaseModel

from schemas.blog import BlogSchema


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class ShowUserSchema(BaseModel):
    name: str
    email: str
    blogs: List[BlogSchema] = []

    class Config:
        orm_mode = True

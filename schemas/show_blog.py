from pydantic import BaseModel

from schemas.show_user import ShowUserSchema


class ShowBlogSchema(BaseModel):
    title: str
    body: str
    author: ShowUserSchema

    class Config:
        orm_mode = True

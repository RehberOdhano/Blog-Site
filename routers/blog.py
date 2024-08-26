from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from repository import blog
from schemas.blog import BlogSchema, ShowBlogSchema

blog_router = APIRouter(prefix="/blog", tags=["Blogs"])


@blog_router.post(
    "/",
    response_model=ShowBlogSchema,
    status_code=status.HTTP_201_CREATED
)
def create_blog(request: BlogSchema, db: Session = Depends(get_db)):
    return blog.add_new_blog(request, db)


@blog_router.get("/all/{id}", response_model=[ShowBlogSchema])
def get_all_blogs_of_a_user(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return blog.get_all_blogs_of_specific_user(user_id, skip, limit, db)

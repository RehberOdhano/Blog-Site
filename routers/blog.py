from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.blog import BlogSchema, ShowBlogSchema
from repository import blog

blog_router = APIRouter(prefix="/blog", tags=["Blogs"])


@blog_router.post(
    "/",
    response_model=ShowBlogSchema,
    status_code=status.HTTP_201_CREATED
)
def create_blog(request: BlogSchema, db: Session = Depends(get_db)):
    return blog.add_new_blog(request, db)

from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.blog import Blog
from schemas.blog import BlogSchema


def add_new_blog(request: BlogSchema, db: Session = Depends(get_db)):
    try:
        new_blog = Blog(**request.model_dump())
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        db.rollback()
        print(f"Error during commit: {e}")
        raise

from fastapi import Depends, status, HTTPException
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

from config.database import get_db
from models.blog import Blog
from models.user import User
from schemas.blog import BlogSchema


def add_new_blog(request: BlogSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {request.user_id} is not found."
            )

        new_blog = Blog(title=request.title, body=request.body, user_id=request.user_id)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise


def get_all_blogs_of_specific_user(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        # Check if the user with the provided id exists or not
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found.")

        # Fetch all the blogs of the user with id 'user_id'
        blogs = db.query(Blog).filter(Blog.user_id == user_id).offset(skip).limit(limit).all()

        if not blogs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No blogs found for this user.")

        return paginate(blogs)
    except Exception as e:
        db.rollback()
        print(f"Error during commit: {e}")
        raise

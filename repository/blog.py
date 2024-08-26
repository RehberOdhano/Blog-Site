from fastapi import Depends, status, HTTPException
from fastapi_pagination import paginate
from sqlalchemy.orm import Session

from config.database import get_db
from enums.response_message import ResponseMessages
from models.blog import Blog
from models.user import User
from schemas.blog import BlogSchema


def add_new_blog(request: BlogSchema, db: Session = Depends(get_db)):
    """
        Adds a new blog to the database.

        1. First it'll check whether the user with the provided id exists or not
        2. If the user exists, then it'll check whether the title of the blog is unique
        3. If the first two conditions satisfies then it'll create and commit the new blog entry.

        If any exception occurs during the process, the transaction will be rolled back to maintain data integrity,
        and the exception is raised.

        Parameters:
        request (BlogSchema): The blog data to be added, including title, body, and user ID.
        db (Session): The database session to be used for querying and committing data.

        Returns:
        Blog: The newly created blog entry.

        Raises:
        HTTPException: If the user with the given ID is not found or if a blog with the same title already exists.
    """
    try:
        # Check if the user with the provided id exists or not
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ResponseMessages.USER_NOT_FOUND.value.format(id=request.user_id)
            )

        # Check if the blog with the same title already exists or not
        blog = db.query(Blog).filter(Blog.title == request.title).first()
        if blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ResponseMessages.BLOG_WITH_SAME_TITLE_ALREADY_EXISTS.value.format(title=request.title)
            )

        # creating new blog and adding to the database
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
    """
        Retrieves all blogs for a specific user from the database with pagination.

        This function performs the following steps:
        1. First it'll check whether the user with the provided id exists or not
        2. If the user exists, then based on that user id, it'll query the database to fetch blogs associated with
        that user, applying pagination with the 'skip' and 'limit' parameters.
        3. If no blogs are found for the user, an HTTP 404 error is raised.
        4. Other-wise returns the paginated list of blogs.

        If any exception occurs during the process, the transaction will be rolled back to maintain data integrity,
        and the exception is raised.

        Parameters:
        user_id (int): The ID of the user whose blogs are to be retrieved.
        skip (int, optional): The number of records to skip for pagination. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
        db (Session): The database session used for querying and committing data.

        Returns:
        List[Blog]: A list of blog entries belonging to the specified user, paginated according to the 'skip'
        and 'limit' parameters.

        Raises:
        HTTPException:
            - If the user with the given ID is not found.
            - If no blogs are found for the specified user.
        Exception: If any other error occurs, it is logged, the transaction is rolled back, and the exception is raised.
    """
    try:
        # Check if the user with the provided id exists or not
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ResponseMessages.USER_NOT_FOUND.value.format(id=user_id)
            )

        # Fetch all the blogs of the user with id 'user_id'
        blogs = db.query(Blog).filter(Blog.user_id == user_id).offset(skip).limit(limit).all()

        if not blogs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ResponseMessages.BLOGS_NOT_FOUND_FOR_THIS_USER.value
            )

        return paginate(blogs)
    except Exception as e:
        db.rollback()
        print(f"Error during commit: {e}")
        raise

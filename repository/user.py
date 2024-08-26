from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from enums.response_message import ResponseMessages
from models.user import User
from schemas.user import UserSchema
from utils.hashing import Hash


def add_new_user(request: UserSchema, db: Session = Depends(get_db)):
    """
        Adds a new user to the database.

        This function performs the following steps:
        1. First it'll check whether the user with the same email already exists or not. If a user with the same email
        address is found, then HTTP 409 Conflict error is raised.
        2. Other-wise, a new user is created with the provided name, email, and a hashed password using bcrypt.
        3. The newly created user will be added to the database and the transaction is committed, and the user object
        is refreshed to reflect the latest state.
        4. Returns the newly created user object.

        If any exception occurs during the process, the transaction will be rolled back to maintain data integrity,
        and the exception is raised.

        Parameters:
        request (UserSchema): The user data to be added, including name, email, and password.
        db (Session): The database session used for querying and committing data.

        Returns:
        User: The newly created user entry.

        Raises:
        HTTPException: If a user with the given email already exists.
        Exception: If any other error occurs, it is logged, the transaction is rolled back, and the exception is raised.
    """
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ResponseMessages.USER_WITH_SAME_EMAIL_ALREADY_EXISTS.value.format(email=request.email),
            )

        new_user = User(
            name=request.name,
            email=request.email,
            password=Hash.bcrypt(request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        raise e

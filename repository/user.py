from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from schemas.user import UserSchema
from utils.hashing import Hash


def add_new_user(request: UserSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == request.email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {request.email} already exists",
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
        print(f"Error: {e}")
        raise e

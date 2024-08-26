from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from repository import user
from schemas.show_user import ShowUserSchema
from schemas.user import UserSchema

user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post(
    "/",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED
)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return user.add_new_user(request, db)

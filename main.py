from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config.database import Base, engine
from routers.blog import blog_router
from routers.user import user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(blog_router)
app.include_router(user_router)

# add pagination to the app
add_pagination(app)

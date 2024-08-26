from fastapi import FastAPI

from utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

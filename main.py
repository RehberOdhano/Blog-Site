from fastapi import FastAPI

from config.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

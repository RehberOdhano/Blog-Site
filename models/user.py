from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    blogs = relationship("Blog", back_populates="author")

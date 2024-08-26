from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from utils.database import Base


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    body = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="blogs")

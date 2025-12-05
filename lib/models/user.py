from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="owner")

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}'>"

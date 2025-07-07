from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

# ORM model for SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # 🔗 One-to-many relationship: user → multiple locations
    locations = relationship("Location", back_populates="user")

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

    class Config:
        orm_mode = True  # ✅ Enables .from_orm(user)






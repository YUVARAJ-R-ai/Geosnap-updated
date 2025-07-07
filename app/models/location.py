from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from pydantic import BaseModel

# ORM model for SQLAlchemy
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # 🔗 Establishes relationship to User model
    user = relationship("User", back_populates="locations")


# Pydantic schema for location creation
class LocationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


# Pydantic schema for location response
class LocationOut(BaseModel):
    name: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True  # ✅ Required for .from_orm() to work in Pydantic v1







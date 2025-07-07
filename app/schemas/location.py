from pydantic import BaseModel

# 🔑 Used when creating a new location (input)
class LocationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

# 👤 Used to represent the associated user in output
class UserOut(BaseModel):
    username: str

    class Config:
        orm_mode = True

# 🗺️ Used when returning location data (output)
class LocationOut(BaseModel):
    name: str
    latitude: float
    longitude: float
    user: UserOut

    class Config:
        orm_mode = True



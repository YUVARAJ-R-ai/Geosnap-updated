from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from app.models.location import Location
from app.db import AsyncSessionLocal
from fastapi import Depends
from utils.security import oauth2_scheme  # if defined there
from utils.jwt import decode_access_token
from app.models.user import User
from app.schemas.location import LocationOut
from app.schemas.location import LocationCreate

import math

router = APIRouter(prefix="/autosnap", tags=["Locations"])


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.post("/create", response_model=LocationOut)
async def create_location(data: LocationCreate, token: str = Depends(oauth2_scheme)):
    try:
    username = decode_access_token(token)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        location = Location(
            name=data.name,
            latitude=data.latitude,
            longitude=data.longitude,
            user_id=user.id
        )
 
        session.add(location)
        await session.commit()
        await session.refresh(location)  # ✅ Ensures full SQLAlchemy object

        return location  # ✅ FastAPI will now use LocationOut.from_orm(location)

except Exception as e:
        print(f"⚠️ Error in /autosnap/create: {e}")
        raise HTTPException(status_code=500, detail=str(e))  # Temporary: shows error in Swagger



@router.get("/getlocations", response_model=dict)
async def getlocations(token: str = Depends(oauth2_scheme)):
    try:
        username = decode_access_token(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        loc_result = await session.execute(select(Location).where(Location.user_id == user.id))
        locations = loc_result.scalars().all()
        return {
            "locations": [
                LocationOut(
                    name=loc.name,
                    latitude=loc.latitude,
                    longitude=loc.longitude,
                    user={"username": user.username}
                )
                for loc in locations
            ]
        }


@router.get("/search")
async def search_locations(query: str = Query(..., min_length=1)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Location).where(Location.name.ilike(f"%{query}%"))
        )
        matches = result.scalars().all()
        return {"results": [loc.name for loc in matches]}

@router.get("/nearby")
async def nearby_locations(lat: float, lng: float, radius_km: float = 5.0):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Location))
        all_locations = result.scalars().all()

        nearby = []
        for loc in all_locations:
            dist = haversine(lat, lng, loc.latitude, loc.longitude)
            if dist <= radius_km:
                nearby.append({"name": loc.name, "distance_km": round(dist, 2)})

        return {"nearby_locations": nearby}











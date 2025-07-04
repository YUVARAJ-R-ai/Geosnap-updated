from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.db import AsyncSessionLocal
from app.models import Location, LocationCreate, User
from app.auth import get_current_user
from app.utils import haversine

router = APIRouter()

# 📦 DB Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 🔒 Secure Create Location Route
@router.post("/")
async def create_location(
    location: LocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_location = Location(
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude,
        user_id=current_user.id  # ✅ Link to user
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return {
        "message": f"Location added by {current_user.username}",
        "location": {
            "name": new_location.name,
            "lat": new_location.latitude,
            "lon": new_location.longitude
        }
    }

# 📍 Get All Locations
@router.get("/")
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location))
    locations = result.scalars().all()
    return {
        "locations": [
            {
                "name": loc.name,
                "lat": loc.latitude,
                "lon": loc.longitude
            }
            for loc in locations
        ]
    }

# 🔍 Search Locations by Name
@router.get("/search")
async def search_locations(name: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Location).where(func.lower(Location.name).like(f"%{name.lower()}%"))
    result = await db.execute(stmt)
    matches = result.scalars().all()
    return {
        "results": [
            {
                "name": loc.name,
                "lat": loc.latitude,
                "lon": loc.longitude
            }
            for loc in matches
        ]
    }

# 📡 Find Nearby Locations
@router.get("/nearby")
async def nearby_locations(
    lat: float,
    lon: float,
    radius_km: float,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Location))
    locations = result.scalars().all()

    nearby = []
    for loc in locations:
        dist = haversine(lat, lon, loc.latitude, loc.longitude)
        if dist <= radius_km:
            nearby.append({
                "name": loc.name,
                "lat": loc.latitude,
                "lon": loc.longitude,
                "distance_km": round(dist, 2)
            })

    return {"results": nearby}

# 🚀 Export router
autosnap_router = router

import asyncio
from app.db import AsyncSessionLocal
from app.models import Location

async def seed():
    async with AsyncSessionLocal() as session:
        locations = [
            Location(name="Marina Beach", latitude=13.0500, longitude=80.2824),
            Location(name="Guindy National Park", latitude=13.0108, longitude=80.2295),
            Location(name="Chennai Central", latitude=13.0827, longitude=80.2707),
        ]
        session.add_all(locations)
        await session.commit()

asyncio.run(seed())

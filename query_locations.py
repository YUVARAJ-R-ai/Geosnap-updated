import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models import Location  # Adjust path if needed

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app/db.sqlite3")
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        result = await session.execute(
            select(Location).where(Location.user_id == 4)
        )
        locations = result.scalars().all()

        print(f"📍 Locations for user_id=4 (jeeva):")
        for loc in locations:
            print(f"• {loc.name} → ({loc.latitude}, {loc.longitude})")

asyncio.run(main())

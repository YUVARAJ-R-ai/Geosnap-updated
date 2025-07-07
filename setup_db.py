from app.db import engine, Base
from app.models.location import Location  # Ensures Location model is registered

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_models())

import asyncio
from app.db import engine
from app.models import Base
from app.models import user  # 👈 this line is critical

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())

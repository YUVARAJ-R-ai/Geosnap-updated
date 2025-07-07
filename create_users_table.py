import asyncio
from app.db import engine
from app.models import Base
import app.models.user  # 👈 ensures User is loaded

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.tables["users"].create(
                bind=sync_conn,
                checkfirst=True
            )
        )

asyncio.run(create_table())

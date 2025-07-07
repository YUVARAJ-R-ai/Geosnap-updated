import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text  # ✅ Add this import

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app/db.sqlite3")

    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")  # ✅ Wrap query in text()
        )
        tables = result.fetchall()
        print("📦 Tables in DB:")
        for table in tables:
            print("-", table[0])

asyncio.run(main())

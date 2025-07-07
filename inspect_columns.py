import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app/db.sqlite3")

    async with engine.connect() as conn:
        def get_columns(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_columns("locations")

        columns = await conn.run_sync(get_columns)
        print("🧬 Columns in 'locations':")
        for col in columns:
            print(f"- {col['name']} ({col['type']})")

asyncio.run(main())

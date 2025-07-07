import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///app/db.sqlite3")

    async with engine.connect() as conn:
        def get_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        tables = await conn.run_sync(get_tables)
        print("Tables in DB:", tables)

asyncio.run(main())

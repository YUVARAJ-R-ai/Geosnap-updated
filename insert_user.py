import asyncio
from app.db import async_session
from app.models.user import User

async def insert_sample_user():
    async with async_session() as session:
        sample = User(
            username="jeevan_test",
            hashed_password="s3cr3tP@ss"
        )
        session.add(sample)
        await session.commit()
        print(f"Inserted user: {sample.username}")

if __name__ == "__main__":
    asyncio.run(insert_sample_user())

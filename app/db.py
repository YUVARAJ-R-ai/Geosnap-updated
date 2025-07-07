from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./geo.db"  # ✅ Using your actual DB

# Create async engine for SQLite
engine = create_async_engine(DATABASE_URL, echo=True)

# Define declarative base for models
Base = declarative_base()

# Create async DB session factory — this is what routes expect
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)





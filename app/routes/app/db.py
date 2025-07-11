import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Detect environment (default to local if not set)
DEPLOY_ENV = os.getenv("DEPLOY_ENV", "local")

# Determine DB path based on environment
if DEPLOY_ENV == "vercel":
    DB_PATH = os.path.join("/tmp", "geo.db")
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "geo.db")

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Optional DB copy logic for Vercel
if DEPLOY_ENV == "vercel":
    SOURCE_DB = os.path.join(os.path.dirname(__file__), "..", "geo.db")

    print(f"SOURCE_DB = {SOURCE_DB}")
    print(f"TARGET_DB = {DB_PATH}")
    print(f"Exists SOURCE? {os.path.exists(SOURCE_DB)}")

    if os.path.exists(SOURCE_DB):
        try:
            import shutil
            shutil.copyfile(SOURCE_DB, DB_PATH)
            print("✅ geo.db copied successfully to /tmp")
        except Exception as e:
            print(f"⚠️ Copy failed: {e}")
    else:
        print("❌ SOURCE_DB not found at runtime!")

# Initialize SQLAlchemy async engine and session
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)





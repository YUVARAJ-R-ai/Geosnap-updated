import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Detect environment
DEPLOY_ENV = os.getenv("DEPLOY_ENV", "local")

# Set DB path based on environment
if DEPLOY_ENV == "vercel":
    DB_PATH = os.path.join("/tmp", "geo.db")
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "geo.db")

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Optional: copy DB to /tmp at runtime
SOURCE_DB = os.path.join(os.path.dirname(__file__), "..", "geo.db")
if DEPLOY_ENV == "vercel" and not os.path.exists(DB_PATH):
    try:
        import shutil
        shutil.copyfile(SOURCE_DB, DB_PATH)
        print("✅ Copied geo.db to /tmp for Vercel")
    except Exception as e:
        print(f"⚠️ Copy failed: {e}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)






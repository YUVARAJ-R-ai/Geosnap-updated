from sqlalchemy.orm import Session
from app.db import engine  # adjust if your engine is elsewhere

def get_session():
    with Session(engine) as session:
        yield session

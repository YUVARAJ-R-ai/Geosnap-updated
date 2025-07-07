from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from utils.security import hash_password, verify_password
from app.models.user import User
from app.db import async_session
from utils.jwt import create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register_user(data: RegisterRequest):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.username == data.username)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        user = User(
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        session.add(user)
        await session.commit()
        return {"message": f"User '{data.username}' registered successfully"}

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.username == form_data.username)
        )
        user = result.scalar_one_or_none()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.username})
        return {
            "access_token": token,
            "token_type": "bearer"
        }

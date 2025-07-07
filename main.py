from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.routes import auth, autosnap

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

app.include_router(auth.router)
app.include_router(autosnap.router)



from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.routes import auth, autosnap

# OAuth2 token setup (used for dependency injection in routes)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Initialize FastAPI app
app = FastAPI()

# Include route modules
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(autosnap.router, prefix="/autosnap", tags=["autosnap"])

# Optional: Health check endpoint for debugging
@app.get("/", tags=["root"])
def root():
    return {"status": "GeoFastAPI is running"}



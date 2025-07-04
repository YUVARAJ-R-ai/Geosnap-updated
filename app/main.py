from fastapi import FastAPI
from app.autosnap import autosnap_router
from app.fallback import fallback_router
from app.auth import router as auth_router

app = FastAPI(title="Geo FastAPI")

app.include_router(autosnap_router, prefix="/autosnap")
app.include_router(fallback_router, prefix="/fallback")
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Geo FastAPI is running"}

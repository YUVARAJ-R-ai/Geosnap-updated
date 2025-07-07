from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.auth import router as auth_router
from app.autosnap import autosnap_router

app = FastAPI(
    title="GeoSnap API",
    description="FastAPI backend for location-based services",
    version="1.0.0"
)

# 🔗 Include routers
app.include_router(auth_router)  # 🔐 /auth/register and /auth/login
app.include_router(autosnap_router, prefix="/autosnap", tags=["Locations"])

# 🚪 Optional root route
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")  # 📘 Redirect to Swagger UI

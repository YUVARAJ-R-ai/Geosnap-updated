from fastapi import APIRouter

fallback_router = APIRouter()

@fallback_router.get("/")
def fallback():
    return {"message": "Fallback endpoint active"}

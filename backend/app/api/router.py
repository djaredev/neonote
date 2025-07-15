from fastapi import APIRouter
from app.api.routes import users, auth, notes, api_docs
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(notes.router)

if settings.ENVIRONMENT == "dev":
    api_router.include_router(api_docs.router)

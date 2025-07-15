from fastapi import FastAPI
from app.api.router import api_router
from app.core.db import create_db_and_tables
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.frontend import frontend

create_db_and_tables()

app = FastAPI(
    openapi_url=f"{settings.API}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API)
app.mount("/", frontend)

from fastapi import FastAPI
from neonote.api.router import api_router
from neonote.core.db import create_db_and_tables
from neonote.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from neonote.core.logger.logger import logger
from neonote.frontend import frontend
from neonote.scripts.prestart import prestart

create_db_and_tables()

app = FastAPI(
    title=settings.API_NAME,
    openapi_url=settings.OPENAPI_URL,
    docs_url=None,
    redoc_url=None,
)

if settings.ENVIRONMENT == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API)
app.mount("/", frontend)

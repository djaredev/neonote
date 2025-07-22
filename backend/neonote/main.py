from fastapi import FastAPI
from neonote.api.router import api_router
from neonote.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from neonote.core.logger.logger import logger
from neonote.frontend import frontend
from neonote.scripts.prestart import prestart

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


def run_server():
    import uvicorn

    prestart()

    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)

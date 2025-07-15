from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings

frontend = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

frontend.mount(
    "/static",
    StaticFiles(directory=settings.FRONTEND_STATIC_PATH),
    name="static",
)


@frontend.get("/favicon.svg")
async def favicon():
    return FileResponse(settings.FRONTEND_FAVICON_PATH, media_type="image/svg+xml")


@frontend.get("/{file_path:path}")
async def root():
    return FileResponse(settings.FRONTEND_INDEX_PATH, media_type="text/html")

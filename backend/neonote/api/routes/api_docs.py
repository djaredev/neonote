from fastapi import APIRouter
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from neonote.core.config import settings

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        title=settings.API_NAME,
        openapi_url=settings.OPENAPI_URL,  # type: ignore
        oauth2_redirect_url="api/docs/oauth2-redirect",
        swagger_favicon_url="/favicon.svg",
    )


@router.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

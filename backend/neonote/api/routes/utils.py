from fastapi import APIRouter


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}

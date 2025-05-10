from fastapi import APIRouter, status
from app.models import UserCreate, UserBase
from app.service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserCreate, service: UserService):
    created_user = service.create_user(user)
    return created_user

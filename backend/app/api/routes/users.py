from fastapi import APIRouter, status
from app.models.user import UserCreate, UserBase
from app.api.deps import SessionDep
from app import service


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserBase)
async def create_user(user: UserCreate, session: SessionDep):
    created_user = service.create_user(user, session)
    return created_user

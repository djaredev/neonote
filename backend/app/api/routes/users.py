from fastapi import APIRouter, status
from app.models.user import UpdatePassword, UserPublic, UserUpdate
from app.service import UserService


router = APIRouter(prefix="/users", tags=["users"])


# @router.post("", status_code=status.HTTP_201_CREATED, response_model=UserBase)
# async def create_user(service: UserService, user: UserCreate):
#     created_user = service.create_user(user)
#     return created_user


@router.patch("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password_me(service: UserService, passwords: UpdatePassword):
    service.update_password(passwords)


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user_me(service: UserService, user_update: UserUpdate):
    updated_user = service.update_user(user_update)
    return updated_user

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import CurrentUser
from app.core.security import create_access_token
from app.models import UserPublic
from app.repository.user_repository import UserRepository
from app.service.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=UserPublic)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    service: AuthService,
    user_repo: UserRepository,
):
    user = service.login(user_repo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user.id)
    response.set_cookie(
        key="neonote_token",
        value=access_token,
        httponly=True,
        secure=False,
    )
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(user: CurrentUser, response: Response):
    response.delete_cookie("neonote_token")


@router.get("/whoami", response_model=UserPublic)
async def whoami(user: CurrentUser):
    return user

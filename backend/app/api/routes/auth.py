from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import UserCookie
from app.core.security import create_access_token
from app.models import UserPublic
from app.service import UserService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=UserPublic)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    userService: UserService,
):
    user = userService.autentication(form_data.username, form_data.password)
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


@router.get("/whoami", response_model=UserPublic)
async def whoami(user: UserCookie):
    return user

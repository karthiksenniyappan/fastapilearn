from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.middleware import no_auth_required
from app.features.users.schema import LoginData, Token, User
from app.features.users.views import UserController

user_router = APIRouter()


# Define a Pydantic model for request body
class LoginRequest(BaseModel):
    username: str
    password: str


@user_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
@no_auth_required()
async def login(request: Request, data: Annotated[LoginData, Depends()]):
    return await UserController.login(request=request, data=data)


@user_router.post('/token/', status_code=status.HTTP_200_OK, response_model=Token)
@no_auth_required()
async def obtain_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    login_user_data = LoginData(email=form_data.username, password=form_data.password)
    return await UserController.login(request=request, data=login_user_data)


@user_router.get("/users/me/", response_model=User)
async def read_users_me(
        request: Request,
        current_user: Annotated[User, Depends(UserController._get_current_user)],
):
    return current_user

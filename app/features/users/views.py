from typing import Annotated

from fastapi import Request, HTTPException, Depends
from sqlmodel import select

# from app.core.views import ModelView
from app.utils.jwt import create_access_token, verify_token
from .auth import verify_password
from .model import User
from .schema import LoginData
from ...core.oauth2_password_bearer import get_oauth2_scheme

_oauth2_scheme = get_oauth2_scheme()


class UserController:
    @staticmethod
    async def login(request: Request, data: LoginData):
        result = await request.app.db.exec(select(User).where(User.email == data.email))
        user = result.first()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        if not user.is_active:
            raise HTTPException(detail='Please Verify Your account', status_code=401)
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def _get_current_user(request: Request, token: Annotated[str, Depends(_oauth2_scheme)]):
        payload = verify_token(token=token, credentials_exception="")
        user = request.state.user
        # add payload.get('user')
        if payload != user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        # token_data = AuthUserSchema(**payload)
        user = await request.app.db.exec(select(User).where(User.email == payload))
        user = user.first()
        if not user.is_active:
            raise HTTPException(detail='Please Verify Your account', status_code=401)
        # returning entire user model but in below current_user property we annotated with CurrentUserSchema
        # it expects only 3 props, that only be get supplied
        # if we want to send the role, create those fields in UserModel and serialize it using schema
        return user

from fastapi import APIRouter
from .endpoints.auth import user_router

v1_api_router = APIRouter(redirect_slashes=False)

v1_api_router.include_router(user_router, prefix="/auth")

from fastapi import APIRouter

from app.api.v1 import v1_api_router

api_router = APIRouter(redirect_slashes=False)

api_router.include_router(router=v1_api_router, prefix='/v1', tags=['V1'])

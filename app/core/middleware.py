from fastapi import Request, HTTPException

import logging
from app.utils.jwt import verify_token


def no_auth_required():
    def decorator(func):
        func.no_auth_required = True
        return func

    return decorator


async def add_user_details_middleware(request: Request):
    endpoint = request.scope.get("endpoint")
    if endpoint and getattr(endpoint, "no_auth_required", False):
        return None  # No auth required for this route

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_data = verify_token(token, 'Invalid token')
    request.state.user = user_data
    return user_data


logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise
    logger.info(f"Request completed: {response.status_code}")
    return response

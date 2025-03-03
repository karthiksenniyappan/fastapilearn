import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import api_router
from app.core.config import settings
from app.core.middleware import add_user_details_middleware, logging_middleware
from app.core.oauth2_password_bearer import get_oauth2_scheme
from app.db.session import async_session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


oauth2_scheme = get_oauth2_scheme()

app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.app.db = async_session()  # Attach async session to app
        response = await call_next(request)
        await request.app.db.close()  # Close async session after request
        return response

app.add_middleware(DBSessionMiddleware)
app.include_router(router=api_router, prefix="/api", dependencies=[Depends(add_user_details_middleware)])

# app.add_middleware(BaseHTTPMiddleware, dispatch=add_user_details_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(HTTPSRedirectMiddleware)
port = settings.PORT | 8090

if __name__ == "__main__":
    can_reload = True if settings.ENVIRONMENT == 'local' else False
    uvicorn.run('main:app', host="0.0.0.0", port=port, reload=can_reload)

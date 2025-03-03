from fastapi.security import OAuth2PasswordBearer


def get_oauth2_scheme():
    """An API URL to get access token from Swagger UI using input fields"""
    return OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token/", auto_error=False)

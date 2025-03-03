from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    is_active: bool = True
    hashed_password: str

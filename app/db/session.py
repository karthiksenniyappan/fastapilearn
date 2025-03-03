import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = settings.DATABASE_URL
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Define a base class for ORM models
Base = declarative_base()

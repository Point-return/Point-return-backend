from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings as sett

DATABASE_URL = sett.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # type: ignore[call-overload]
    expire_on_commit=False,
)

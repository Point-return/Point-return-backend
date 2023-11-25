from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings as sett


SQLALCHEMY_DATABASE_URL = (
        f"{sett.DB_ENG}+asyncpg://{sett.PG_USER}:{sett.PG_PASS}"
        + f"@{sett.DB_HOST}:{sett.DB_PORT}/{sett.DB_NAME}"
    )

DATABASE_URL = SQLALCHEMY_DATABASE_URL

engine = create_async_engine(
    DATABASE_URL
)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass

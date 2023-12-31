import sys

from app.config import settings
from app.core.models import Base
from app.database import engine
from app.products.models import *  # noqa: F401, F403
from app.users.models import *  # noqa: F401, F403


async def drop_database() -> None:
    """Drop database."""
    assert settings.MODE == 'DEV'

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(drop_database())

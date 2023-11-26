from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта."""

    DB_PORT: int
    PG_PASS: str
    PG_USER: str
    DB_ENG: str
    DB_NAME: str
    DB_HOST: str

    class Config:
        env_file = '.env'

    @property
    def DATABASE_URL(cls):
        """Создание URL для базы данных в зависимости от .env файла.

        Returns:
            URL базы данных.
        """
        if cls.DB_ENG == 'sqlite':
            return f'{cls.DB_ENG}+aiosqlite:///{cls.DB_NAME}.db'
        return (
            f'{cls.DB_ENG}+asyncpg://{cls.PG_USER}:{cls.PG_PASS}'
            + f'@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'
        )


settings = Settings()

API_URL = '/api/v1'

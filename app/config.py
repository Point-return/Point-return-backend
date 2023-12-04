import logging
from logging.config import dictConfig
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Настройки проекта."""

    model_config = SettingsConfigDict(env_file='.env')

    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_PORT: int
    PG_PASS: str
    PG_USER: str
    DB_ENG: str
    DB_NAME: str
    DB_HOST: str

    @property
    def DATABASE_URL(cls) -> str:
        """Создание URL для базы данных в зависимости от .env файла.

        Returns:
            URL базы данных.
        """
        return (
            f'{cls.DB_ENG}+asyncpg://{cls.PG_USER}:'
            f'{cls.PG_PASS}@{cls.DB_HOST}:'
            f'{cls.DB_PORT}/{cls.DB_NAME}'
        )

    TEST_DB_PORT: int
    TEST_PG_PASS: str
    TEST_PG_USER: str
    TEST_DB_ENG: str
    TEST_DB_NAME: str
    TEST_DB_HOST: str

    @property
    def TEST_DATABASE_URL(cls) -> str:
        """Создание URL для базы данных в зависимости от .env файла.

        Returns:
            URL базы данных.
        """
        return (
            f'{cls.TEST_DB_ENG}+asyncpg://{cls.TEST_PG_USER}:'
            f'{cls.TEST_PG_PASS}@{cls.TEST_DB_HOST}:'
            f'{cls.TEST_DB_PORT}/{cls.TEST_DB_NAME}'
        )

    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()

API_URL = '/api/v1'
TOKEN_NAME = 'access_token'
DATA_IMPORT_LOCATION = str(BASE_DIR / 'data')


class CSVFilenames:
    """Названия файлов с тестовыми данными."""

    products: str = 'marketing_product'
    dealers: str = 'marketing_dealer'
    parsed_data: str = 'marketing_dealerprice'
    product_dealer: str = 'marketing_productdealerkey'


class Roles:
    """Используемые в проекте роли."""

    user: str = 'user'
    admin: str = 'admin'


LOGGER_NAME = 'point_logger'


class LoggingConfig(BaseModel):
    """Конфигурация логирования."""

    LOGGER_NAME: str = LOGGER_NAME
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = 'DEBUG'

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: Dict[str, Dict[str, str]] = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers: Dict[str, Dict[str, str]] = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers: Dict[str, Dict[str, Any]] = {
        LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
    }


dictConfig(LoggingConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)

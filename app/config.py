from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_PORT: int
    PG_PASS: str
    PG_USER: str
    DB_ENG: str
    DB_NAME: str
    DB_HOST: str

    class Config:
        env_file = '.env'


settings = Settings()

API_URL = '/api/v1'

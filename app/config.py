from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    DB_PORT: int
    PG_PASS: str
    PG_USER: str
    DB_ENG: str
    DB_NAME: str
    DB_HOST: str

    class Config:
        env_file = '.env'
    
    @root_validator
    def get_database_url(cls, v):
        if v['DB_ENG'] == 'sqlite':
            v['DATABASE_URL'] = f"{v['DB_ENG']}+aiosqlite:///{v['DB_NAME']}.db"
        else:
            v['DATABASE_URL'] = (
                    f"{v['DB_ENG']}+asyncpg://{v['PG_USER']}:{v['PG_PASS']}"
                    + f"@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
                )
        return v


settings = Settings()

API_URL = '/api/v1'

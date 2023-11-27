from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    """Класс регистрации пользователей."""

    email: EmailStr
    password: str
    username: str

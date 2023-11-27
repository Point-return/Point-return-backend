from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    """Схема регистрации пользователей."""

    email: EmailStr
    password: str
    username: str


class UserSafe(BaseModel):
    """Схема отображения пользователя без пароля."""

    email: EmailStr
    username: str

    class Config:
        orm_mode = True

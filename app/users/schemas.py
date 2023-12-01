from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    """Схема регистрации пользователей."""

    email: EmailStr = Field(..., alias='email')
    password: str = Field(..., alias='password')
    username: str = Field(..., alias='username')


class UserSafe(BaseModel):
    """Схема отображения пользователя без пароля."""

    email: EmailStr = Field(..., alias='email')
    username: str = Field(..., alias='username')

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    """Схема для отображения токена."""

    access_token: str = Field(..., alias='access_token')

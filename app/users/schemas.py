from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.schemas import to_snake_case


class UserAuth(BaseModel):
    """Схема регистрации пользователей."""

    model_config = ConfigDict(alias_generator=to_snake_case)

    email: EmailStr
    password: str
    username: str


class UserSafe(BaseModel):
    """Схема отображения пользователя без пароля."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )

    email: EmailStr
    username: str


class TokenSchema(BaseModel):
    """Схема для отображения токена."""

    model_config = ConfigDict(alias_generator=to_snake_case)

    access_token: str

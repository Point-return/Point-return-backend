from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.schemas import to_snake_case


class UserRegister(BaseModel):
    """User registration scheme."""

    model_config = ConfigDict(alias_generator=to_snake_case)

    email: EmailStr
    password: str
    username: str


class UserLogin(BaseModel):
    """User registration scheme."""

    model_config = ConfigDict(alias_generator=to_snake_case)

    email: EmailStr
    password: str


class UserSafe(BaseModel):
    """User display scheme without password."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_snake_case,
    )

    id: int
    email: EmailStr
    username: str


class TokenSchema(BaseModel):
    """Scheme for displaying a token."""

    accessToken: str

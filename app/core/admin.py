from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import TOKEN_NAME, Roles, settings
from app.users.auth import authenticate_user_by_username, create_access_token


class AdminAuth(AuthenticationBackend):
    """Аутентификация в админ-зоне."""

    async def login(self, request: Request) -> bool:
        """Вход в админ-зону.

        Args:
            request: передаваемый запрос.

        Returns:
            Возможность войти в админ-зону.
        """
        form = await request.form()
        username, password = form.get('username'), form.get('password')
        user = await authenticate_user_by_username(
            username,  # type: ignore[arg-type]
            password,  # type: ignore[arg-type]
        )
        if not user:
            return False
        if user.role != Roles.admin:
            return False
        access_token = create_access_token({'sub': str(user.id)})
        request.session.update({TOKEN_NAME: access_token})
        return True

    async def logout(self, request: Request) -> bool:
        """Выход из админ-зоны.

        Args:
            request: передаваемый запрос.

        Returns:
            True
        """
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Аутентификация в админ-зоне.

        Args:
            request: передаваемый запрос.

        Returns:
            Наличие токена
        """
        token = request.session.get(TOKEN_NAME)
        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
from app.core.dao import BaseDAO
from app.users.models import User


class UserDAO(BaseDAO):
    """Интерфейс работы с моделями пользователей."""

    model = User

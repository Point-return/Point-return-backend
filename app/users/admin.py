# mypy: disable-error-code="list-item, assignment"
from sqladmin import ModelView

from app.users.models import User


class UserAdmin(ModelView, model=User):
    """Представление пользователя в admin-зоне."""

    column_list = [User.id, User.username, User.email]
    column_details_exclude_list = [User.password]
    name = 'Пользователь'
    name_plural = 'Пользователи'

# mypy: disable-error-code="list-item, assignment"
from sqladmin import ModelView

from app.users.models import User


class UserAdmin(ModelView, model=User):
    """Представление пользователя в admin-зоне."""

    column_list = [User.id, User.username, User.email]
    column_details_exclude_list = [User.password]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.email]
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'

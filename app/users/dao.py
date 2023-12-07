from app.core.dao import BaseDAO
from app.users.models import User


class UserDAO(BaseDAO):
    """Interface for working with user models."""

    model = User

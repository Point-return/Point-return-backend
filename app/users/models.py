from sqlalchemy import Column, Integer, String

from app.core.models import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self) -> str:
        """Функция для представления модели пользователя.

        Returns:
            Строку с именем пользователя.
        """
        return f'User {self.username}'

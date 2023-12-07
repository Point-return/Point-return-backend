from sqlalchemy import Column, Integer, String

from app.core.models import Base


class User(Base):
    """User model."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __repr__(self) -> str:
        """Represent the user model.

        Returns:
            Username string.
        """
        return f'User {self.username}'

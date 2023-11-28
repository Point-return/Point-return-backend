import sys
from getpass import getpass

from email_validator import EmailNotValidError, validate_email

from app.config import Roles
from app.users.auth import get_password_hash
from app.users.dao import UserDAO
from app.users.exceptions import (
    UserEmailAlreadyExistsException,
    UserNameAlreadyExistsException,
)


async def create_admin() -> None:
    """Функция для создания админа."""
    try:
        print(  # noqa: T201
            'В любой момент нажмите ctrl+C для прекращения создания админа',
        )
        while True:
            try:
                email = input('Введите почту:\n')
                validate_email(email)
                existing_user_email = await UserDAO.find_one_or_none(
                    email=email,
                )
                if not existing_user_email:
                    break
                else:
                    print(UserEmailAlreadyExistsException.detail)  # noqa: T201
            except EmailNotValidError:
                print('Email не валидный')  # noqa: T201
        while True:
            username = input('Введите имя пользователя:\n')
            existing_user_name = await UserDAO.find_one_or_none(
                username=username,
            )
            if not existing_user_name:
                break
            else:
                print(UserNameAlreadyExistsException.detail)  # noqa: T201
        hashed_password = get_password_hash(getpass('Введите пароль:\n'))
        await UserDAO.create(
            email=email,
            password=hashed_password,
            username=username,
            role=Roles.admin,
        )
        print('Админ успешно создан!')  # noqa: T201
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_admin())

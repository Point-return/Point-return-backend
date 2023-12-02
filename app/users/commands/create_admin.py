import sys
from getpass import getpass

from email_validator import EmailNotValidError, validate_email

from app.config import Roles
from app.main import logger
from app.users.auth import get_password_hash
from app.users.dao import UserDAO
from app.users.exceptions import (
    UserEmailAlreadyExistsException,
    UserNameAlreadyExistsException,
)


async def create_admin() -> None:
    """Функция для создания админа."""
    try:
        logger.debug(
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
                    logger.debug(UserEmailAlreadyExistsException.detail)
            except EmailNotValidError:
                logger.debug('Email не валидный')
        while True:
            username = input('Введите имя пользователя:\n')
            existing_user_name = await UserDAO.find_one_or_none(
                username=username,
            )
            if not existing_user_name:
                break
            else:
                logger.debug(UserNameAlreadyExistsException.detail)
        while True:
            password1 = getpass('Введите пароль:\n')
            password2 = getpass('Повторите пароль:\n')
            if password1 == password2:
                hashed_password = get_password_hash(password1)
                break
            else:
                logger.debug('Пароли не совпадают')
        await UserDAO.create(
            email=email,
            password=hashed_password,
            username=username,
            role=Roles.admin,
        )
        logger.debug('Админ успешно создан!')
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_admin())

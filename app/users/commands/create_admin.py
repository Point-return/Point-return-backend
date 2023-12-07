import sys
from getpass import getpass

from email_validator import EmailNotValidError, validate_email

from app.config import Roles, logger
from app.users.auth import get_password_hash
from app.users.dao import UserDAO
from app.users.exceptions import (
    UserEmailAlreadyExistsException,
    UserNameAlreadyExistsException,
)


async def create_admin() -> None:
    """Create an admin-user."""
    try:
        logger.debug(
            'At any time, press ctrl+C to stop creating an admin',
        )
        while True:
            try:
                email = input('Enter your email:\n')
                validate_email(email)
                existing_user_email = await UserDAO.find_one_or_none(
                    email=email,
                )
                if not existing_user_email:
                    break
                else:
                    logger.debug(UserEmailAlreadyExistsException.detail)
            except EmailNotValidError:
                logger.debug('Email is not valid')
        while True:
            username = input('Enter your username:\n')
            existing_user_name = await UserDAO.find_one_or_none(
                username=username,
            )
            if not existing_user_name:
                break
            else:
                logger.debug(UserNameAlreadyExistsException.detail)
        while True:
            password1 = getpass('Enter password:\n')
            password2 = getpass('Repeat password:\n')
            if password1 == password2:
                hashed_password = get_password_hash(password1)
                break
            else:
                logger.debug('Password mismatch')
        await UserDAO.create(
            email=email,
            password=hashed_password,
            username=username,
            role=Roles.admin,
        )
        logger.debug('Administrator has been created successfully!')
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(create_admin())

from base64 import b64encode
from secrets import token_bytes
from random import randint

from app.config import logger


def generate_secret_key() -> str:
    """Create a secret key.

    Returns:
        An example of a random secret key.
    """
    return b64encode(token_bytes(32)).decode()


def create_code() -> str:
    """Генератор 6-и значного ключа."""
    return str(randint(1000000, 9999999))[1::]


if __name__ == '__main__':
    logger.debug(generate_secret_key())

from base64 import b64encode
from secrets import token_bytes

from app.config import logger


def generate_secret_key() -> str:
    """Create a secret key.

    Returns:
        An example of a random secret key.
    """
    return b64encode(token_bytes(32)).decode()


if __name__ == '__main__':
    logger.debug(generate_secret_key())

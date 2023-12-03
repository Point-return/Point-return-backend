from base64 import b64encode
from secrets import token_bytes
from random import randint


def generate_secret_key() -> str:
    """Функция для создания секретного ключа.

    Returns:
        Пример случайного секретного ключа.
    """
    return b64encode(token_bytes(32)).decode()


def create_code() -> str:
    """Генератор 6-и значного ключа."""
    return str(randint(1000000, 9999999))[1::]


if __name__ == '__main__':
    print(generate_secret_key())  # noqa: T201

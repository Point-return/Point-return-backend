from base64 import b64encode
from secrets import token_bytes


def generate_secret_key() -> str:
    """Функция для создания секретного ключа.

    Returns:
        Пример случайного секретного ключа.
    """
    return b64encode(token_bytes(32)).decode()


if __name__ == '__main__':
    print(generate_secret_key())  # noqa: T201

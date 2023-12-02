from math import trunc
from typing import Optional


def convert_string_to_float(string: str) -> Optional[float]:
    """Функция для преобразования строки в float.

    Args:
        string: передаваемая строка.

    Returns:
        Число с плавающей запятой или None, если строка пустая.
    """
    if not string:
        return None
    return float(string)


def convert_to_float_and_truncate(string: str) -> Optional[int]:
    """Функция для преобразования строки в int с отбросанной дробной частью.

    Args:
        string: передаваемая строка.

    Returns:
        Целое число с отбросанной дробной частью или None, если строка пустая.
    """
    if not string:
        return None
    return trunc(float(string))

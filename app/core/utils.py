from math import trunc
from typing import Optional


def convert_string_to_float(string: str) -> Optional[float]:
    """Transform string to float.

    Args:
        string: passed string.

    Returns:
        Floating point number or None if string is empty.
    """
    if not string:
        return None
    return float(string)


def convert_to_float_and_truncate(string: str) -> Optional[int]:
    """Transform a string to an int with the fractional part removed.

    Args:
        string: passed string.

    Returns:
        Integer with fractional part removed, or None if string is empty.
    """
    if not string:
        return None
    return trunc(float(string))

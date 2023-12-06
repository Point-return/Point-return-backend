from datetime import datetime
from typing import Optional


def date_val(
    year: int,
    month: int,
    day: int,
) -> Optional[datetime]:
    """Program for validation date."""
    if year < 1900:
        year = 1900
    if year > 2100:
        year = 2100
    if month < 1:
        month = 1
    if month > 12:
        month = 12
    if day < 1:
        day = 1
    if day > 31:
        day = 31
    try:
        return datetime(int(year), int(month), int(day))
    except ValueError:
        return None

from pydantic import BaseModel


def to_snake_case(string: str) -> str:
    """Format string to snake_case.

    Args:
        string: provided string.

    Returns:
        string in snake case.
    """
    return ''.join(
        ['_' + i.lower() if i.isupper() else i for i in string],
    ).lstrip('_')


class EmptySchema(BaseModel):
    """Empty response schema."""

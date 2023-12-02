from fastapi import HTTPException, status

ParsedDataNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Parsing data not found',
)

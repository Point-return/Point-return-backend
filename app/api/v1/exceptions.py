from fastapi import HTTPException, status

ParsedDataNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Parsing data not found',
)

ConnectionAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='the data key has already been selected',
)

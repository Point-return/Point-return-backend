from fastapi import HTTPException, status

ParsedDataNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Parsing data not found',
)

ConnectionAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Data key has already been selected',
)

DealerNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Dealer not found',
)

ProductNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Product not found',
)

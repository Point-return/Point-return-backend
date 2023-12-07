from fastapi import HTTPException, status

ParsedDataNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Parsing data not found',
)

DealerNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Dealer not found',
)

ProductNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Product not found',
)

ProductDealerNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Product-dealer connection not found',
)
DateError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Invalid date!',
)

from fastapi import HTTPException, status

UserNameAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='A user with the same name already exists',
)

UserEmailAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='A user with this email already exists',
)

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Wrong data',
)

NoTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token not provided',
)

WrongTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token',
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token has expired',
)

UserInfoNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='No data from token',
)

WrongUserInfoException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token data is incorrect',
)

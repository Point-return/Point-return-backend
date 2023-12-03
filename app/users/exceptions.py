from fastapi import HTTPException, status

UserNameAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с таким именем уже существует',
)

UserEmailAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь с такой почтой уже существует',
)

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Неверные данные',
)

NoTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен не предоставлен',
)

WrongTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный токен',
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек',
)

UserInfoNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Данные из токена отсутствуют',
)

WrongUserInfoException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Данные из токена неверны',
)

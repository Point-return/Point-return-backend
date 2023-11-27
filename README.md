# Проект Point-return-backend

### Описание:

Проект Point-return-backend - ... .

### Как установить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Point-return/Point-return-backend.git
cd Point-return-backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source venv/bin/activate
```

Одновить pip и установить зависимости из файла requirements.txt:

```
make pip
make req
```

Для работы приложения необходим файл .env:

```
touch .env
```

Необходимо заполнить файл .env следующим обазом:

```
DB_ENG=postgresql
Название базы данных на английском для подключения (Разработка велать на PostgreSQL)

PG_USER=
Имя пользователя базы данных postgres.

PG_PASS=
Пароль пользователя базы данных postgres.

DB_NAME=
Имя базы данных.

DB_HOST=
Адрес связи с базой данных.

DB_PORT=
Порт связи с базой данных.

SECRET_KEY = 
Секретный ключ для генетации JWT-токена.

ALGORITHM = 
Алгоритм для генетации JWT-токена.

```

### Как запустить бэкенд без контейнеров:

Выполнить миграции:

```
make migration name=Migration_name
make migrate
```

Запустить приложение:

```
make run
```

### Эндпоинты:

| Эндпоинт                             |Тип запроса | Тело запроса | Ответ           |
|--------------------------------------|------------|--------------|-----------------|
|/                                     |GET         |              |```"Hello"```    |

### Стек технологий использованный в проекте:

- Python
- FastAPI
- PostgreSQL
- SQL Alchemy
- SQL Admin

### Авторы:

- :white_check_mark: [vlad3069](https://github.com/vlad3069)
- :white_check_mark: [Starkiller2000Turbo](https://github.com/Starkiller2000Turbo)

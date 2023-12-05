# Проект Point-return-backend

### Описание:

Проект Point-return-backend - ... .

### Как установить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Point-return/Point-return-backend.git
cd Point-return-backend
```

Cоздать и активировать виртуальное окружение для Windows:

```
python -m venv venv
source venv/Scripts/activate
```

Для Linux:

```
python3 -m venv venv
source venv/bin/activate
```

Обновить pip:

```
make pip
```

Файлы зависимости разделяются по следующим назначениям:

```
requirements.txt - требования для работы backend основы приложения
make req

requirements-DS.txt - требования для работы DS-скрипта (обязательны при запуске)
make ds-req

requirements-style.txt - требования для стилизации кода при разработке
make style-req

requirements-test.txt - требования для работы тестирования
make test-req
```

Для запуска будет достаточно установить зависимости, требуемые для backend-основы и DS-скрипта:
```
make base-req
```

Для работы приложения необходим файл .env:

```
touch .env
```

Необходимо заполнить файл .env следующим обазом:

```

MODE = DEV / TEST / PROD
Режим работы приложения. DEV - разработка, TEST - тестирование, PROD - продакшн

DB_ENG=postgresql
Название базы данных на английском для подключения (Разработка велась на PostgreSQL)

PG_USER=
Имя пользователя базы данных postgresql.

PG_PASS=
Пароль пользователя базы данных postgresql.

DB_NAME=
Имя базы данных.

DB_HOST=
Адрес связи с базой данных.

DB_PORT=
Порт связи с базой данных.

TEST_DB_ENG=postgresql
Название тестовой базы данных на английском для подключения (Разработка велась на PostgreSQL)

TEST_PG_USER=
Имя пользователя тестовой базы данных postgresql.

TEST_PG_PASS=
Пароль пользователя тестовой базы данных postgresql.

TEST_DB_NAME=
Имя тестовой базы данных.

TEST_DB_HOST=
Адрес связи с тестовой базой данных.

TEST_DB_PORT=
Порт связи с тестовой базой данных.

SECRET_KEY = 
Секретный ключ для генетации JWT-токена.

ALGORITHM = 
Алгоритм для генетации JWT-токена.

```
Для генерации секретного ключа можно воспользоваться следующей командой:
```
make secret-key
```
После генерации вставьте ключ в файл .env указанным образом.

### Подготовка файлов с данными:

Чтобы заполнить данными систему, необходимо использовать 4 файла с расширением csv.
Разместить их необходимо в папке data, расположенной внутри папки app. 

```
cd app
cd data
```

Необходимые названия файлов указаны в файле app.config в классе CSVFiles. 
По умолчанию названия файлов указаны далее.

#### Файл продуктов marketing_product.csv:

|Заголовок  | Пустой столбец      | id     |    article |   ean_13    | name  | cost |  recommended_price   |   category_id |   ozon_name   |name_1c    |   wb_name |   ozon_article    |   wb_article  |ym_article |   wb_article_td   |
|---------|-------|-------|-------|----------|------|-----|-----------------|------------|---------|-------|-------|------------|--------- |----------|-------------|
| Тип     | Integer  |  Integer |   String |    BigInteger  |   String  |   Float   |   Float   | Integer    | String  |    String | String | Integer     | Integer  | String   | String      |

#### Файл дилеров marketing_dealer.csv:

| Заголовок | id    |	name    |
|-----------|-------|-----------|
| Тип       |Integer| String    |

#### Файл связок продукт-дилер marketing_productdealerkey.csv:

| Заголовок | id     |	key    |	dealer_id  |	product_id    |
|-----------|--------|---------|---------------|------------------|
| Тип       |Integer |String   | Integer       |     Integer      |

id	product_key	price	product_url	product_name	date	dealer_id

#### Файл данных парсинга marketing_dealerprice.csv:

| Заголовок | id     |	product_key |	price |	product_url |	product_name |	date          |	dealer_id   |
|-----------|--------|--------------|---------|-------------|----------------|----------------|-------------|
| Тип       |Integer | String       | Float   | String      | String         | Date  %Y-%m-%d | Integer     |

Импортировать данные можно следующей командой, предварительно вернувшись в корневую директорию:

```
cd ..
cd ..
make import
```

Также предусмотрен импорт отдельно каждой таблицы. 
Однако импорт product-dealer требует наличия products и dealers, а импорт parsed-data - product-dealer и dealers:
```
make products
make dealers
make product-dealer
make parsed-data
```
### Как запустить backend без контейнеров:

Выполнить миграции:

```
make migration name=Migration_name
make migrate
```
Создайте админа:
```
make admin
```

Запустить приложение:

```
make run
```

## Тестирование приложения

Для запуска тестов в директории app/data необходимо расположить файл с названием по умолчанию mock_users.csv. 
Необходимо добавить одного пользователя с ролью admin, одного - с ролью user.

#### Файл тестовых данных mock_users.csv:

| Заголовок | username     |	email       |	password    |	role        |
|-----------|--------------|----------------|---------------|---------------|
| Тип       |   String     | Email String   | String        | admin / user  |

Для запуска тестов можно использовать 2 команды:

```
make test
pytest
```

### Эндпоинты:

Документация на эндпоинты при локальном запуске располагается по адресу: http://127.0.0.1:8000/docs


### Стек технологий использованный в проекте:

- CSV
- FastAPI
- FuzzyWuzzy
- Pandas
- PostgreSQL
- Pydantic
- Pytest
- Python
- SQLAlchemy
- SQLAlchemy Admin
- Swagger
- Uvicorn

### Авторы backend-основы:

- :white_check_mark: [Maksim Ermoshin](https://github.com/Starkiller2000Turbo)
- :white_check_mark: [Vladislav Podtiazhkin](https://github.com/vlad3069)

### Авторы DS-скрипта:

- :white_check_mark: [Aigerim Tokhmetova](https://github.com/moonkerimka)
- :white_check_mark: [Aleksandr Filippov](https://github.com/AlexFee1)
- :white_check_mark: [Evgeniy Bessonov](https://github.com/evgeniy-yandex)

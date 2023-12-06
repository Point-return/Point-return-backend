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

Импортировать данные можно следующей командой:

```
make import
```

Также предусмотрен импорт отдельно каждой таблицы:
```
make products
make dealers
make product-dealer
make parsed-data
```
### Как запустить бэкенд без контейнеров:

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

### Эндпоинты:

| Эндпоинт                             |Тип запроса | Тело запроса | Ответ           |
|--------------------------------------|------------|--------------|-----------------|
|/                                     |GET         |              |```"Hello"```    |

### Стек технологий использованный в проекте:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- SQLAlchemy Admin
- CSV
- Scarlette
- Pydantic
- Swagger

<p align="left">
<a href="https://www.python.org/" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/python-colored.svg" width="45" height="45" alt="Python" /></a>
<a href="https://www.postgresql.org/" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/postgresql-colored.svg" width="45" height="45" alt="PostgreSQL" /></a>
<a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/skills/fastapi-colored.svg" width="45" height="45" alt="Fast API" /></a>
<a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="45" height="45"/> </a> 
<a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="45" height="45"/> </a>
<a href="https://www.nginx.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="45" height="45"/> </a> 
<a href="https://www.sqlalchemy.org/" class="external-link" target="_blank"> <img src="https://avatars.githubusercontent.com/u/6043126?s=48&v=4" alt="sqlalchemy" width="45" height="45"/> </a>
<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank"> <img src="https://avatars.githubusercontent.com/u/110818415?s=48&v=4" alt="pydantic" width="45" height="45"/> </a>
<a href="https://www.swagger.io/" target="_blank" rel=”noopener”> <img src="https://cdn.svgporn.com/logos/swagger.svg" alt="swagger" width="45" height="45"/> </a>
<a href="https://www.github.com/" target="_blank" rel=”noopener”>  <img src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" alt="swagger" width="45" height="45"/> </a> 
</p>

### Авторы:

- :white_check_mark: [vlad3069](https://github.com/vlad3069)
- :white_check_mark: [Starkiller2000Turbo](https://github.com/Starkiller2000Turbo)

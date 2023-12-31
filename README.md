# Project Point-return-backend

![example workflow](https://github.com/Point-return/Point-return-backend/actions/workflows/main.yml/badge.svg)

Links:
- :white_check_mark: [API Documentation](https://point-return.sytes.net/api/v1/docs/)
- :white_check_mark: [Complete project](https://point-return.github.io/)

### Description:

The Point-return-backend project is a project developed on the modern FastApi web framework to develop a solution to automate the process of comparing goods. Offering several customer products that are most likely to match the dealer's marked product. Implementing this solution as an online service that opens in a web browser.

### How to install a project:

Clone the repository and go to it on the command line:

```
git clone git@github.com:Point-return/Point-return-backend.git
cd Point-return-backend
```

Create and activate a virtual environment for Windows:

```
python -m venv venv
source venv/Scripts/activate
```

For Linux:

```
python3 -m venv venv
source venv/bin/activate
```

Update pip:

```
make pip
```

Dependency files are separated according to the following purposes:

```
requirements.txt - requirements for running the backend basics of the application
make req

requirements-DS.txt - requirements for the DS script to work (required when starting)
make ds-req

requirements-style.txt - requirements for styling code during development
make style-req

requirements-test.txt - requirements for testing work
make test-req
```

To start, just install the dependencies required for the backend framework and the DS script:
```
make base-req
```

For the application to work, a .env file (or server.env file for containers) is required:

```
touch .env
touch server.env
```

You need to fill out the .env (server.env) file with the following:

```

MODE=DEV / TEST / PROD
Application operating mode. DEV - development, TEST - testing, PROD - production

DB_ENG=postgresql
Name of the database for connection (Development was carried out in PostgreSQL)

PG_USER=
Postgresql database username.

PG_PASS=
Postgresql database user password.

DB_NAME=
Database name.

DB_HOST=
Database HOST address.

DB_PORT=
Database communication PORT.

TEST_DB_ENG=postgresql
Name of the test database for connection (Development was carried out in PostgreSQL)

TEST_PG_USER=
Postgresql test database username.

TEST_PG_PASS=
Postgresql test database user password.

TEST_DB_NAME=
Test database name.

TEST_DB_HOST=
HOST address for connecting to the test database.

TEST_DB_PORT=
Communication PORT with test database.

SECRET_KEY=
Secret key for generating a JWT token.

ALGORITHM=
Algorithm for generating a JWT token.

POSTGRES_USER=
Username that will be set when creating a postgresql database to access it
Should be equal to PG_USER

POSTGRES_PASSWORD=
Password that will be set when creating a postgresql database to access it
Should be equal to PG_PASS

POSTGRES_DB=
The name of created postgresql database
Should be equal to DB_NAME
```
To generate a secret key, you can use the following command:
```
make secret-key
```
After generation, paste the key into the .env file as specified.

### Preparing data files:

To fill the system with data, you need to use 4 files with the csv extension.
They must be placed in the data folder located inside the app folder.

```
cd app
cd data
```

The required file names are specified in the app.config file in the CSVFilenames class.
By default, the file names are listed below.

#### Products file marketing_product.csv:

| Heading  | Empty column      | id     |    article |   ean_13    | name  | cost |  recommended_price   |   category_id |   ozon_name   |name_1c    |   wb_name |   ozon_article    |   wb_article  |ym_article |   wb_article_td   |
|---------|-------|-------|-------|----------|------|-----|-----------------|------------|---------|-------|-------|------------|--------- |----------|-------------|
| Type     | Integer  |  Integer |   String |    BigInteger  |   String  |   Float   |   Float   | Integer    | String  |    String | String | Integer     | Integer  | String   | String      |

#### Dealer File marketing_dealer.csv:

| Heading | id    |	name    |
|-----------|-------|-----------|
| Type       |Integer| String    |

#### Product-dealer link file marketing_productdealerkey.csv:

| Heading | id     |	key    |	dealer_id  |	product_id    |
|-----------|--------|---------|---------------|------------------|
| Type       |Integer |String   | Integer       |     Integer      |

#### Parsing data file marketing_dealerprice.csv:

| Heading | id     |	product_key |	price |	product_url |	product_name |	date          |	dealer_id   |
|-----------|--------|--------------|---------|-------------|----------------|----------------|-------------|
| Type       |Integer | String       | Float   | String      | String         | Date  %Y-%m-%d | Integer     |

You can import data with the following command, after first returning to the root directory:

```
cd ../..
make import
```

It is also possible to import each table separately.
However, the product-dealer import requires products and dealers, and the parsed-data import requires product-dealer and dealers:
```
make products
make dealers
make product-dealer
make parsed-data
```
### How to run backend without containers:

Run migrations:

```
make migration name=Migration_name
make migrate
```
Create an admin:
```
make admin
```

Launch the application:

```
make run
```

The application will be available via this address:
```
127.0.0.1:8000
```

### How to run backend using containers:

Run following command:
```
make docker
```

This command would build all workers according to the files on your PC.
Or you can use following command, which would use pre-created images:
```
make production
```

The application will be available via this address:
```
localhost:8000
```

## Application testing

To run tests, you need to place in app/data a number of csv files, which names are specified in app/tests/conftest.py file in filenames fixture. Default file names are listed below. For users file You need to add one user with the admin role, and one with the user role.

#### Test data file test_users.csv:

| Heading   | username     |	email       |	password    |	role        |
|-----------|--------------|----------------|---------------|---------------|
| Type      |   String     | Email String   | String        | admin / user  |

#### Products file test_products.csv:

| Heading  | id     |    article |   ean_13    | name  | cost |  recommended_price   |   category_id |   ozon_name   |name_1c    |   wb_name |   ozon_article    |   wb_article  |ym_article |   wb_article_td   |
|---------|-------|-------|----------|------|-----|-----------------|------------|---------|-------|-------|------------|--------- |----------|-------------|
| Type     |  Integer |   String |    BigInteger  |   String  |   Float   |   Float   | Integer    | String  |    String | String | Integer     | Integer  | String   | String      |

#### Dealer File test_dealer.csv:

| Heading | id    |	name    |
|---------|-------|---------|
| Type    |Integer| String  |

#### Product-dealer link file test_productdealer.csv:

| Heading |	key    |	dealer_id  |	product_id    |
|---------|--------|---------------|------------------|
| Type    |String  | Integer       |     Integer      |

#### Parsing data file test_dealerprice.csv:

| Heading | id     |price    |	product_url |	product_name |	date          |	dealer_id   |
|---------|--------|---------|--------------|----------------|----------------|-------------|
| Type    |Integer | Float   | String       | String         | Date  %Y-%m-%d | Integer     |

To run tests you can use next command. It not obly starts tests, but also creates coverage report.

```
make report
```

To read coverage report you can use one of two commands:

```
make read-report
coverage report
```

### Technology stack used in the project:

- CSV
- Docker
- Docker Compose
- Github Actions
- Gunicorn
- FastAPI
- FuzzyWuzzy
- Nginx
- Pandas
- PostgreSQL
- Pydantic
- Pytest
- Python
- SQLAlchemy
- SQLAlchemy Admin
- Swagger
- Uvicorn

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

### Authors of the backend framework:

- :white_check_mark: [Maksim Ermoshin](https://github.com/Starkiller2000Turbo)
- :white_check_mark: [Vladislav Podtiazhkin](https://github.com/vlad3069)

### Authors of the frontend framework:

- :white_check_mark: [Amir Mukhtarov](https://github.com/m0000Amir)
- :white_check_mark: [Ilya Biryulev](https://github.com/IlyaBiryulev)

### Authors of the DS script:

- :white_check_mark: [Aigerim Tokhmetova](https://github.com/moonkerimka)
- :white_check_mark: [Aleksandr Filippov](https://github.com/AlexFee1)
- :white_check_mark: [Evgeniy Bessonov](https://github.com/evgeniy-yandex)

### Links to archives:

- :white_check_mark: [Link to code from the main repository](https://drive.google.com/file/d/1Ij-8dj7bJrDjM27wdOqIHsenWml131i6/view?usp=sharing)
- :white_check_mark: [Link to screen Swagger UI](https://drive.google.com/file/d/1d1s4TAFXJE4ihbzgvtL6X1kTvy1cgJlL/view?usp=sharing)

WORKDIR = app
current_dir = $(shell pwd)

ifeq ($(OS),Windows_NT)
    PYTHON = python
	PIP = pip
else
    PYTHON = python3
	PIP = pip3
endif

# starting

default:
	make migration name="Initial"
	make migrate
	make run

migration:
	@alembic revision --autogenerate -m "$(name)"

migrate:
	@alembic upgrade head

admin:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/users/commands/create_admin.py

run:
	@uvicorn app.main:app

# requirements

pip:
	@$(PYTHON) -m $(PIP) install --upgrade pip

req:
	@$(PIP) install -r requirements.txt

ds-req:
	@$(PIP) install -r requirements-DS.txt

style-req:
	@$(PIP) install -r requirements-style.txt

test-req:
	@$(PIP) install -r requirements-test.txt

base-req:
	@make req
	@make ds-req

all-req:
	@make req
	@make style-req
	@make ds-req
	@make test-req

# styling

style:
	isort $(WORKDIR)
	black -S -l 79 $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

# utils

secret-key:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/core/commands/generate_key.py

# data

products:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/products/commands/import_products.py

dealers:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/products/commands/import_dealers.py

product-dealer:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/products/commands/import_productdealer.py

parsed-data:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/products/commands/import_parsed_data.py

import:
	@make dealers
	@make products
	@make product-dealer
	@make parsed-data

drop:
	@PYTHONPATH=$(current_dir) $(PYTHON) app/core/commands/drop_database.py
# testing

test:
	pytest

report:
	coverage run -m pytest app

read-report:
	coverage report


# docker

make compose:
	docker compose up --build -d

make production:
	docker compose -f docker-compose.production.yml up --build -d

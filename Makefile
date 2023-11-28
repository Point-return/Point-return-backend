WORKDIR = app
MAIN = $(WORKDIR)/main.py
current_dir = $(shell pwd)

default:
	make migration name="Initial"
	make migrate
	make run

style:
	isort $(WORKDIR)
	black -S -l 79 $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

migration:
	@alembic revision --autogenerate -m "$(name)"

migrate:
	@alembic upgrade head

admin:
	@PYTHONPATH=$(current_dir) python app/users/commands/create_admin.py

run:
	@uvicorn app.main:app --reload

pip:
	@python -m pip install --upgrade pip

req-file:
	@pip freeze -> requirements.txt

req:
	@pip install -r requirements.txt

style-req:
	@pip install -r style-requirements.txt

secret-key:
	@python app/core/generate_key.py

products:
	@PYTHONPATH=$(current_dir) python app/products/commands/import_products.py

dealers:
	@PYTHONPATH=$(current_dir) python app/products/commands/import_dealers.py

product-dealer:
	@PYTHONPATH=$(current_dir) python app/products/commands/import_productdealer.py

parsed-data:
	@PYTHONPATH=$(current_dir) python app/products/commands/import_parsed_data.py

import:
	@make products
	@make dealers
	@make product-dealer
	@make parsed-data

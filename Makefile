WORKDIR = app
MAIN = $(WORKDIR)/main.py

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
	alembic revision --autogenerate -m "$(name)"

migrate:
	alembic upgrade head

run:
	uvicorn app.main:app

pip:
	python -m pip install --upgrade pip

req-file:
	pip freeze -> requirements.txt

req:
	pip install -r requirements.txt

style-req:
	pip install -r style-requirements.txt

secret-key:
	python app/core/generate_key.py
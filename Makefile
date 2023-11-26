WORKDIR = app
MAIN = $(WORKDIR)/main.py

default:
	python $(MAIN)

style:
	isort $(WORKDIR)
	black -S -l 79 $(WORKDIR)
	flake8 $(WORKDIR)
	mypy $(WORKDIR)

migrations:
	alembic revision --autogenerate -m "$(name)"

run:
	uvicorn app.main:app --reload

pip:
	python -m pip install --upgrade pip

req-file:
	pip freeze -> requirements.txt

req:
	pip install -r requirements.txt

style-req:
	pip install -r style-requirements.txt

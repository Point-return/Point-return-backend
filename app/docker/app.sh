#!/bin/bash

make migration

make migrate

make admin

make import

gunicorn app.main:app --workers 5 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

#!/bin/bash
cd /root/app
make migrate
make import
gunicorn app.main:app --workers 5 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

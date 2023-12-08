#!/bin/bash
cd /root/app
make migrate
make import
gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

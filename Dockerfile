FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY requirements-DS.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt --no-cache-dir
RUN python -m pip install -r requirements-DS.txt --no-cache-dir
COPY . .
RUN chmod +x ./app/docker/app.sh

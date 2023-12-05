FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY requirements-DS.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -r requirements-DS.txt --no-cache-dir
COPY . .
RUN chmod a+x /app/app/docker/app.sh

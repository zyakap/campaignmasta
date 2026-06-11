FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIPENV_VENV_IN_PROJECT=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv

COPY Pipfile* ./
RUN pipenv install --skip-lock || pipenv install --deploy

COPY . .

RUN mkdir -p /app/media /app/staticfiles /app/static_files /app/logs /app/uploads

EXPOSE 8031

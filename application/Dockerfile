# FROM python:3.11-alpine3.19
FROM python:3.11-slim

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg libsm6 libxext6 \
    software-properties-common && \
    export PKG_NAME=$(ls dist/ | head -n 1) && \
    sed -i "s|hands-to-text = {path = \"../package\"}|hands-to-text = {path = \"dist/$PKG_NAME\"}|" pyproject.toml && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry update && \
    poetry install --only main && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["gunicorn", "app:application"]
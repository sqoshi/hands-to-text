FROM python:3.11-slim

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH" \
    HANDS_MODEL_PATH="/app/models/hands"

WORKDIR /app

COPY /application ./application
COPY /package ./package
COPY /models ./models

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ffmpeg libsm6 libxext6 \
    software-properties-common && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["gunicorn", "app:application"]
FROM python:3.11-slim

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH" \
    HANDS_MODEL_PATH="/app/models/hands"


COPY /application ./application
COPY /package ./package
COPY /models ./models

WORKDIR /application

SHELL ["/bin/sh", "-euo", "pipefail", "-c"]
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    ffmpeg libsm6 libxext6 \
    software-properties-common && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["gunicorn", "application"]
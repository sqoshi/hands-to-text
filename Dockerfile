FROM python:3.11-slim
ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH" \
    HANDS_MODEL_PATH="/app/models/hands"


WORKDIR /app

COPY /application ./application
COPY /package ./package
COPY /models ./models

WORKDIR /app/application

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl ffmpeg git libsm6 libxext6 \
    software-properties-common && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["gunicorn", "application"]
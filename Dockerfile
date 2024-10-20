FROM ghcr.io/sqoshi/htt-models:0.0.0 AS models

FROM python:3.12-slim AS base

ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV PATH="/app/.venv/bin:$PATH" \
    HANDS_PATH=/app/models/rf.pickle

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential curl ffmpeg git libsm6 libxext6 software-properties-common  && \
    rm -rf /var/lib/apt/lists/*

FROM base AS builder
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_DYNAMIC_VERSIONING_COMMANDS=""

WORKDIR /app

COPY /package ./package
COPY /webapp ./webapp
COPY --from=models /models ./models

# WORKDIR /app/package

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry self add "poetry-dynamic-versioning[plugin]"
    #  && \
    # poetry install --only main

WORKDIR /app/webapp

RUN poetry install --only main

FROM base AS final
ENV PATH="/app/webapp/.venv/bin:/app/package/.venv/bin:$PATH"

COPY --from=builder /app /app

WORKDIR /app/webapp/httfe

ENTRYPOINT ["uvicorn", "main:app"]

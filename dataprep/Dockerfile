FROM python:3.11-slim
ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH" 

WORKDIR /app

COPY . .

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["httdataprep", "--help"]
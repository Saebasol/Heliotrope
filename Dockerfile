FROM python:3.13 AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs

COPY pyproject.toml poetry.lock poetry.toml ./

RUN pip install poetry

RUN poetry install --no-interaction --only main

FROM python:3.13-slim AS production

WORKDIR /app

COPY ./heliotrope ./heliotrope

COPY --from=builder ./.venv ./.venv

ENTRYPOINT [".venv/bin/python", "-m", "heliotrope"]
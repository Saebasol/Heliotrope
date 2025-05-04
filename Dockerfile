FROM python:3.13-slim AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY ./heliotrope ./heliotrope

COPY pyproject.toml poetry.lock poetry.toml ./

RUN poetry install --no-interaction --only main

ENTRYPOINT [".venv/bin/python", "-m", "heliotrope"]
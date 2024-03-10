# This image is meant to be used with docker compose

FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

ENV PYTHONUNBUFFERED 1

RUN pip install pipx

RUN pipx install poetry

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-root
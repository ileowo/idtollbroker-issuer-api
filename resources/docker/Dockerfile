# syntax=docker/dockerfile:1
FROM python:3.10.6-slim-buster

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update and install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.1.15

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

ARG DJANGO_SUPERUSER_PASSWORD
ARG DJANGO_SUPERUSER_EMAIL
ARG DJANGO_SUPERUSER_USERNAME

ENV DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD}
ENV DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL}
ENV DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME}

RUN chmod 777 /app/resources/docker/entrypoint.sh

RUN mv /app/resources/docker/entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "pob_backend.wsgi"]
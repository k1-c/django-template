FROM python:3.8-slim as builder

WORKDIR usr/src/app

RUN pip install poetry

COPY /src /app/poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt


FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR usr/src/app

COPY --from=builder usr/src/app/requirements.txt usr/src/app/requirements.txt

RUN pip install -r usr/src/app/requirements.txt

COPY /src .

EXPOSE 8000

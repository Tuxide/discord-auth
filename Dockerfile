# Generate requirements.txt
FROM python:3.8 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# Install app
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV MODULE_NAME "app.main"

COPY scripts.py prestart.sh /app/
COPY app /app/app
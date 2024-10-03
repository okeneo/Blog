FROM python:3.12.2-slim-bookworm

RUN adduser --disabled-password --no-create-home myuser

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

RUN pip install --upgrade pip

COPY requirements.txt /api/
RUN pip install -r requirements.txt

COPY . /api

RUN chmod +x ./entrypoint-api.sh
RUN chmod +x ./entrypoint-celery.sh

RUN chown -R myuser:myuser /api

USER myuser

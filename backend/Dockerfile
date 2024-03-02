FROM python:3.12.2-slim-bookworm

RUN adduser --disabled-password --no-create-home myuser

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

RUN pip install --upgrade pip

COPY requirements.txt /backend/
RUN pip install -r requirements.txt

COPY . /backend

RUN chmod +x ./entrypoint-api.sh
RUN chmod +x ./entrypoint-celery.sh

RUN chown -R myuser:myuser /backend

USER myuser

FROM python:3.12.2-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY . /backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
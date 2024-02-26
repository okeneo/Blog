FROM python:3.12.2-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY requirements.txt /backend/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /backend

EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000"]

# Blog API

> This is a Blog REST API built using Django and the Django REST framework. It is hosted on an AWS EC2 instance but I do not keep it available all the time due to the limitations of the AWS free-tier plan. When it is available, it can be accessed [here](https://tegaokene.com/api/swagger).


## Features

- **[Swagger Docs](https://okeneo.github.io/BlogAPI/) API documentation**
- JSON Web Token (JWT) for authentication
- Nginx as a reverse proxy
- Redis for caching
- Throttling to prevent abuse
- Free SSL certificates using Certbot (for HTTPS)
- Comprehensive unit tests


## API Documentation

A sample of the static API documentation is hosted on [GitHub Pages](https://okeneo.github.io/BlogAPI/). When the production API is live, the documentation can be found [here](https://tegaokene.com/api/swagger) and you can interact with it like any other API.


## Technologies Used

- Django and Django REST framework (DRF)
- Docker
- AWS (EC2, RDS, Route53)
- Nginx
- Redis
- JSON Web Token (JWT)
- PostgreSQL
- Certbot for HTTPS


## Requirements
- Python 3.11.8 or higher
- Docker 24.0.7 or later
- A `.env.dev` or `.env.prod` file located in the root directory


## Environment Variable Template

```
# Django
SECRET_KEY="your-default-secret-key"
DJANGO_ALLOWED_HOSTS="127.0.0.1 localhost"
DEBUG=1 # For development ONLY

# Django DB settings
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="yourdb"
DB_USER="youruser"
DB_PASSWORD="yourpassword"
DB_HOST="db"
DB_PORT="5432"

# PostgreSQL on Docker
POSTGRES_USER="youruser"
POSTGRES_PASSWORD="yourpassword"
POSTGRES_DB="yourdb"
```

## Setup

This project is designed to run with Docker. However, you can also run the Django application independently (using the [Setup Django](#setup-django) instructions), which is often convenient during development. This means, however, that Nginx will no longer serve as a revere proxy, and Redis will need to be started manually. Additionally, in a production environment, you will no longer have Certbot for HTTPS. It is also important to know that the Django (development) server is not even designed for use in a production environment, as seen [here](https://docs.djangoproject.com/en/5.1/ref/django-admin/#runserver).


## Setup (Docker)

1. Clone the repository:

   ```bash
   git clone https://github.com/okeneo/BlogAPI.git
   ```

2. Build the Docker images:

   ```bash
   docker-compose -f docker-compose.dev.yml build
   ```

3. Start the containers:

   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

4. In a separate terminal, run the following command to collect static files for Django to serve:

   ```bash
   docker exec -it blogapi-api-1 python manage.py collectstatic --no-input
   ```

## Setup (Django)

1. Clone the repository:

   ```bash
   git clone https://github.com/okeneo/BlogAPI.git
   ```

2. Navigate to the project directory:

    ```bash
    cd BlogAPI
    ```

3. Create, then activate a virtual environment (Recommended):

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

4. Install dependencies:

    ```bash
    cd api
    python -m pip install -r requirements.txt
    ```

5. Apply migrations

    ```bash
    python manage.py migrate
    ```

6. Start the server:

    ```bash
    python manage.py runserver
    ```

## Running tests

1. Navigate to the api directory:

    ```bash
    cd BlogAPI
    cd api
    ```

2. Run unit test Django command:

    ```bash
    python manage.py test
    ```


## Contact
- [Email](okenetega@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/tega-okene/)

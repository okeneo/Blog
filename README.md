# Personal Website

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/okeneo/PersonalNest/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/okeneo/PersonalNest.svg)](https://github.com/okeneo/PersonalNest/issues)

This website serves as a portfolio and place to showcase my projects, skills, and experiences. It also includes a blog section.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Contact](#contact)

## Features

- [Swagger Docs](https://okeneo.github.io/PersonalNest/) API documentation.
- Blog section for tutorials and sharing my thoughts.
  - Includes signup and login with JWT authentication.
- Comprehensive unit tests.

## Technologies Used

- Django
- React
- Docker
- AWS
- Nginx
- Django REST framework
- Redis + Celery
- JSON Web Token (JWT)
- PostgreSQL

## Requirements
- Python 3.11.8
- Docker 24.0.7

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/okeneo/PersonalNest.git
   ```

### Backend Setup

1. Navigate to the project directory:

    ```bash
    cd PersonalNest
    ```
2. Create, then activate a Virtual Environment (Optional):

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. Install Dependencies:

    ```bash
    cd backend
    python -m pip install -r requirements.txt
    ```

4. Apply Migrations

    ```bash
    python manage.py migrate
    ```

5. Extra Setup:

    ```
    Set DEBUG=True in settings.py if necessary
    ```

### Frontend Setup

## Contact
- Email: okenetega@gmail.com
- LinkedIn: https://www.linkedin.com/in/tega-okene/

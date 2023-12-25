# PersonalNest
Includes a blog.
## Setup for local development

### Set up a virtual environment
```shell script
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies
```shell script
python -m pip install -r requirements.txt
```

### Migrate Database
```shell script
python manage.py migrate
```

### Extra setup work
* Set ```DEBUG=True``` if necessary
* Add ```127.0.0.1``` to ```ALLOWED_HOSTS```

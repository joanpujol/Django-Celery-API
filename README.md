# Cartloop Test

Backend Challenge for Cartloop. Django REST API + Celery.

## How to set up
This installation guide presumes that you have virtualenvwrapper and docker installed on your system.
```bash
git clone git@github.com:joanpujol/testcartloop.git
cd testcartloop
# Make a new virtualenv
mkvirtualenv testcartloop -p `which python3.8`
pip install -r requirements/requirements.txt
python manage.py migrate

# In order to access the /admin/ panel which will enable you to create some needed model instances:
python manage.py createsuperuser
```

## How to run
All the following must be run in different terminals so that they can work together.
```bash
# How to run the REST API
python manage.py runserver

# How to run RabbitMQ
docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

# How to run a Celery scheduler
celery -A testcartloop.celery beat

# How to run a Celery worker
celery -A testcartloop.celery worker --loglevel=info
```

## How to test
The conversationss app contains a tests module which includes 3 test cases:
- Endpoint tests
- Scheduler module tests
- Celery task test
```bash
# From the project directory run:
python manage.py test conversations
```

## Configurations
From setting.py you can change the following configs:
- MAX_MESSAGES_PER_HOUR
- SENDING_INTERVAL_START
- SENDING_INTERVAL_END

celery.py contains the crontab schedule that will activate the celery beat once an hour.

## Additional notes
- Some validation has been added accorded to the specification, it's located in the validators.py module within the conversations app.
- A new model has been added for GroupOperator, which was hinted in the operator model specification but was not in the list explicitly.

# Email Scheduler App

## Setup up the environment
- Install Python 3+
- Set Environment, run:
```
python3 -m venv venv
```
- Install dependencies on local environment
```
make dependencies
```
- Install Docker and Docker Compose or Docker Desktop

## Directory structure
```
email_scheduler/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── email_sender.py
│   ├── static/
│   └── templates/
├── migrations/
├── Dockerfile
├── docker-compose.yml
├── config.py
├── Makefile
├── README.md
├── .gitignore
└── requirements.txt
```

## Running the app
To start the application, run:
```
make build
```

To rebuild the applicatoin, run:
```
make rebuild
```

To shutdown the application, run:
```
make down
```

To start Celery Beat *(if not already running)*:
```
make celery-beat
```

## Running the migration
To init migration, run:
```
make migrate-init
```

To migrate, run:
```
make migrate
```

To upgrade migration, run:
```
make migrate-upgrade
```

To bundle all at the same time, run:
```
make migrate-all
```

## Running the test
To start the test, run:
```
export PYTHONPATH=$(pwd)
make test
```

## How to test locally
Please access `http://localhost:8080` 

- You can try via GUI

- Or API via Postman to create schedule email
```
curl --location 'http://localhost:8080/api/save_emails' \
--header 'Content-Type: application/json' \
--data-raw '{
    "recipients": "hi@local.com, hello@local.com",
    "event_id": 1,
    "email_subject": "Schedule Email",
    "email_content": "This is schedule email content",
    "timestamp": "2024-10-17 15:00:00",
    "timezone": "Asia/Singapore"
}'
```
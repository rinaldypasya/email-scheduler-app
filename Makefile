build:
	docker-compose up --build

down:
	docker-compose down

celery-beat:
	docker-compose up celery-beat

migrate-init:
	docker-compose run web flask db init

migrate:
	docker-compose run web flask db migrate

migrate-upgrade:
	docker-compose run web flask db upgrade

migrate-all:
	migrate-init
	migrate
	migrate-upgrade

test:
	pytest

dependencies:
	pip3 install --no-cache-dir -r requirements.txt

rebuild:
	make down
	make build
	migrate-upgrade
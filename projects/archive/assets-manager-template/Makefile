.PHONY: help build up down logs clean restart shell db-init

help:
	@echo "Assets Manager - Available Commands"
	@echo "===================================="
	@echo "make build       - Build Docker images"
	@echo "make up          - Start containers"
	@echo "make down        - Stop containers"
	@echo "make logs        - View container logs"
	@echo "make restart     - Restart containers"
	@echo "make shell       - Access app container shell"
	@echo "make clean       - Clean up Docker resources"
	@echo "make db-init     - Initialize database"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Application running at http://localhost:5000"

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose restart

shell:
	docker-compose exec app /bin/bash

clean:
	docker-compose down -v
	docker system prune -f

db-init:
	docker-compose exec app python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"

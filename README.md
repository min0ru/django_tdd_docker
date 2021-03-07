# Tutorial Project: Test-Driven Development with Django, Django REST Framework and Docker

[![pipeline status](https://gitlab.com/min0ru/django_tdd_docker_ci/badges/master/pipeline.svg)](https://gitlab.com/min0ru/django_tdd_docker_ci/commits/master) [![coverage report](https://gitlab.com/min0ru/django_tdd_docker_ci/badges/master/coverage.svg)](https://gitlab.com/min0ru/django_tdd_docker_ci/-/commits/master)

## Development environment deployment

### Requirements for dev environment

```bash
sudo apt install docker.io docker-compose
```

Optional requirements (for running application without dockerized environment)


```
pyenv (for installing different python versions)
pipenv (managing python virtual environments and packages)
```

### Environment variables

Create .env.dev file with example development configuration:

```dotenv
POSTGRES_DB=movies_dev
POSTGRES_USER=movies
POSTGRES_PASSWORD=movies
SECRET_KEY=DEBUG_SECRET_KEY
DEBUG=1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=movies_dev
DB_USER=movies
DB_PASSWORD=movies
DB_HOST=movies-db
DB_PORT=5432
DJANGO_ALLOWED_HOSTS=*
```

### Docker-Compose Dev Environment

Build and run docker-compose environment:

```bash
docker-compose up --build -d
```

Check docker containers up and running:

```bash
docker-compose ps
```

Check containers logs:

```bash
docker-compose logs -f
```

Shut down development enironment:

```bash
docker-compose down -v
```

### Application

After running docker-compose environment application will be available with links provided:

Smoke test endpoint: http://localhost:8000/ping/

API endpoints: http://localhost:8000/api/

OpenAPI v2 documentation (swagger): http://localhost:8000/swagger/

CoreAPI documentation: http://localhost:8000/docs/

### Testing

Run tests in dockerized environment:

```bash
docker-compose up --build -d
docker-compose exec movies pytest
```

Run tests with coverage report

```bash
docker-compose up --build -d
docker-compose exec movies pytest --cov
```

### Code Quality Control 

Run code quality checks:

```bash
docker-compose exec movies flake8 .
docker-compose exec movies black . --check
docker-compose exec movies isort . --check-only
```

Automatic formating and imports sorting:
```bash
docker-compose exec movies black .
docker-compose exec movies isort .
```

### Production Deployment

Automatic CI/CD available with provided GitLab CI config (.gitlab-ci.yml).

Check Django settings.py file for other configurable environment variables.


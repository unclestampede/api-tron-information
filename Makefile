include .env
export


# Docker
d_up: docker_up
docker_up:
	docker-compose up --build

d_b: docker_build
docker_build:
	docker-compose build --no-cache api


## Format all
fmt: format
format: isort black


## Check code quality
chk: check
lint: check
check: flake black_check isort_check

mypy:
	mypy app tests

## Tests
tests: test
test:
	pytest --asyncio-mode=auto -v

cov: coverage
coverage:
	coverage run -m pytest --asyncio-mode=auto -v && coverage report -m

## Sort imports
isort:
	isort app tests

isort_check:
	isort --check-only app tests


## Format code
black:
	black --config pyproject.toml app tests

black_check:
	black --config pyproject.toml --diff --check app tests


# Check pep8
flake:
	flake8 --config .flake8 app tests


# Migrations
create_migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

run:
	gunicorn app:app

test:
	py.test --cov-report term-missing --cov=api --cov=models --cov=utils tests/

migrate:
	alembic upgrade head || alembic stamp head

flake_test:
	flake8 . --count --statistics

.PHONY: run, test, flake_test

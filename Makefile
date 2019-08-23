run:
	gunicorn app:app

test:
	py.test --cov-report term-missing --cov=api --cov=models tests/

.PHONY: run, test

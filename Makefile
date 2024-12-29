# Makefile
.PHONY: run lint test

run:
	python server.py

lint:
	pipenv run pylint .

test:
	pipenv run python -m unittest discover -s tests


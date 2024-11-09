# Environment Setup
VENV := env
REQUIREMENTS := requirements.txt

# Python interpreter
PYTHON := python

#server
SERVER := uvicorn

.PHONY: set-venv venv install run test coverage lint clean

set-venv:
	$(PYTHON) -m venv $(VENV)

venv:
	.\$(VENV)\Scripts\activate

install: venv
	pip install -r $(REQUIREMENTS)

run:
	$(SERVER) src.api.main:app --reload --workers 4

test: venv install
	pytest tests

coverage: venv install test
	coverage run -m pytest tests
	coverage report tests

lint-check:
	black . --check
	isort . --check

lint:
	black .
	isort .

clean:
	rm -rf .\.pytest_cache _pycache__
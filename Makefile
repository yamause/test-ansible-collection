.DEFAULT_GOAL := install

.PHONY: install
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	ansible-galaxy install -r requirements.yml
	pre-commit install

.PHONY: lint
lint:
	ansible-lint
	yamllint .

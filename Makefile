defualt: ## Run app
	@. ./venv/bin/activate && FLASK_APP=northstar/__init__.py FLASK_ENV=development flask run

activate: ## Slip into virtual environment
	@-virtualenv venv
	. ./venv/bin/activate

coverage:
	@ . ./venv/bin/activate  && coverage run -m pytest
	@ . ./venv/bin/activate  && coverage html
	@ . ./venv/bin/activate  && coverage xml

doc: ## Generate documentation
	@-rm -rf dist
	@-mkdir -p dist/openapi/
	@cd ./docs/openapi/  && yarn install && yarn html
	@cp -r ./docs/openapi/dist/* dist/openapi/

env: ## Install all dependencies
	@-virtualenv venv
	. ./venv/bin/activate && pip install -r requirements.txt

freeze: ## Freeze python dependencies
	@. ./venv/bin/activate && pip freeze > requirements.txt

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

i: ## Launch app.py in an interactive python shell
	python -i ./northstar/__init__.py

lint: ## Run linter
	@./venv/bin/black ./northstar/*
	@./venv/bin/black ./tests/*

migrate: ## Run migrations
	. ./venv/bin/activate && yoyo develop

test: ## Run tests
	@cd ./docs/openapi/  && yarn install 
	@cd ./docs/openapi/  && yarn test 
	@pip install -e .
	@pip install '.[test]'
	@./venv/bin/pytest

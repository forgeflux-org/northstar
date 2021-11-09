default: ## Run app
	@. ./venv/bin/activate && python -m northstar

coverage:
	@ . ./venv/bin/activate  && coverage run -m pytest
	@ . ./venv/bin/activate  && coverage html
	@ . ./venv/bin/activate  && coverage xml

doc: ## Generate documentation
	@-rm -rf dist
	@-mkdir -p dist/openapi/
	@cd ./docs/openapi/  && yarn install && yarn html
	@cp -r ./docs/openapi/dist/* dist/openapi/

docker: ## Build Docker image from source
	docker build -t forgedfed/northstar .

env: ## Install all dependencies
	@-virtualenv venv
	. ./venv/bin/activate && pip install -r requirements.txt
	. ./venv/bin/activate && pip install -e .
	. ./venv/bin/activate && pip install '.[test]'

freeze: ## Freeze python dependencies
	@. ./venv/bin/activate && pip freeze > requirements.txt
	@-sed -i 's/northstar.*/.\//' requirements.txt

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

i: ## Launch app.py in an interactive python shell
	python -i ./northstar/__init__.py

lint: ## Run linter
	@./venv/bin/black ./northstar/*
	@./venv/bin/black ./tests/*

migrate: ## Run migrations
	@. ./venv/bin/activate && FLASK_APP=northstar/app.py FLASK_ENV=development flask migrate

test: ## Run tests
	@cd ./docs/openapi/  && yarn install 
	@cd ./docs/openapi/  && yarn test 
	@. ./venv/bin/activate && pip install -e .
	@. ./venv/bin/activate && pip install '.[test]'
	@./venv/bin/pytest
	@pip uninstall -y northstar

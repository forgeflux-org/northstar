defualt: ## Run app
	@. ./venv/bin/activate && FLASK_APP=src/app FLASK_ENV=development flask run

activate: ## Slip into virtual environment
	@-virtualenv venv
	. ./venv/bin/activate

freeze:
	@. ./venv/bin/activate && pip freeze > requirements.txt

env: ## Install all dependencies
	@-virtualenv venv
	. ./venv/bin/activate && pip install -r requirements.txt

i: ## Launch app.py in an interactive python shell
	python -i ./src/app.py

lint: ## Run linter
	./venv/bin/black ./src/*
	@cd ./docs/openapi/ && yarn run spectral lint api/*

test: ## Run tests
	@cd ./docs/openapi/  && yarn install 
	@cd ./docs/openapi/  && yarn test 

doc: ## Generate documentation
	@-rm -rf dist
	@-mkdir -p dist/openapi/
	@cd ./docs/openapi/  && yarn install && yarn html
	@cp -r ./docs/openapi/dist/* dist/openapi/

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

defualt: ## Run app
	@source ./venv/bin/activate && FLASK_APP=src/app FLASK_ENV=development flask run

activate: ## Slip into virtual environment
	source ./venv/bin/activate

deps-freeze:
	@source ./venv/bin/activate && pip freeze > requirements.txt

deps-install: ## Install all dependencies
	source ./venv/bin/activate && pip install -r requirements.txt

i: ## Launch app.py in an interactive python shell
	python -i ./src/app.py

lint: ## Run linter
	./venv/bin/pylint ./src/*

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

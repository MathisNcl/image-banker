.DEFAULT_GOAL := help
.PHONY: help
.EXPORT_ALL_VARIABLES:

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 _]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Code 
deps: # Install deps
	pip install -e .[all]
pre: # Run pre-commit hooks on all files and clear output jupyter
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace development/*.ipynb && pre-commit run --all-files
cov: # Compute coverage
	pytest --cov=src --cov-report term-missing --browser=chrome --headless
app: # Launch app
	streamlit run src/image_banker/app.py


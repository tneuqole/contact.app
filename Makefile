.PHONY: init
init:
	uv add --dev ruff isort pynvim

.PHONY: venv
venv:
	source .venv/bin/activate

.PHONY: fmt
fmt:
	-uv run ruff check --fix
	uv run isort .
	uv run ruff format

.PHONY: run
run:
	uv run flask --app app run

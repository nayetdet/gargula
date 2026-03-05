.PHONY: install api db-up db-down db-revision

install:
	uv sync --all-groups --all-packages

api:
	uv run uvicorn gargula.main:app --host 0.0.0.0 --port 8000 --reload

db-up:
	uv run alembic upgrade head

db-down:
	uv run alembic downgrade -1

db-revision:
	uv run alembic revision --autogenerate -m "$(m)"

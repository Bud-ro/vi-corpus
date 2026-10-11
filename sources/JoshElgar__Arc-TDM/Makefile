.PHONY: install-backend install-frontend install dev-api dev-ui smoke check

install-backend:
	cd backend && python3 -m venv .venv && .venv/bin/python -m pip install -e ".[dev]"

install-frontend:
	cd frontend && npm ci

install: install-backend install-frontend

dev-api:
	cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000

dev-ui:
	cd frontend && npm run dev

smoke:
	cd backend && .venv/bin/python -m pytest tests/test_smoke.py

check:
	cd backend && .venv/bin/python -m ruff check .
	cd backend && .venv/bin/python -m pytest
	cd frontend && npm run build

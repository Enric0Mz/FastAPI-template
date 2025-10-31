# ==============================================================================
# Variables
# ==============================================================================

# Use 'poetry run' to execute commands within the project's virtual environment
VENV_RUN = poetry run

# Source code directories
SRC_DIR = src
TEST_DIR = tests

# FastAPI application entry point
APP_MODULE = src.main:app

# Docker-compose service name for the local database
DB_SERVICE = db-local

# Default message for new migrations (can be overridden)
# Usage: make migrate-new M="add user table"
M ?= new migration

# Migrations directory
MIGRATIONS_DIR = src/infra/


# ==============================================================================
# Phony Targets (Commands that don't produce files)
# ==============================================================================

.PHONY: help all install run test format lint check db-up db-down db-logs clean migrate migrate-new


# ==============================================================================
# Help
# ==============================================================================

# Default target: show help
all: help

help:
	@echo "Makefile for FastAPI Project"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Project & Dependencies:"
	@echo "  install    - Install Python dependencies using Poetry."
	@echo "  clean      - Remove .pyc files and __pycache__ directories."
	@echo ""
	@echo "Local Development:"
	@echo "  run        - Run the FastAPI app locally with auto-reload."
	@echo "  test       - Run the test suite using pytest."
	@echo "  format     - Auto-format code with 'black'."
	@echo "  lint       - Lint code with 'ruff'."
	@echo "  check      - Run 'lint' and 'format' (in check mode)."
	@echo ""
	@echo "Docker Services (Database):"
	@echo "  db-up      - Start the local Postgres container (${DB_SERVICE}) in the background."
	@echo "  db-down    - Stop and remove all containers defined in docker-compose."
	@echo "  db-logs    - View the logs for the local database container."
	@echo ""
	@echo "Migrations (Alembic):"
	@echo "  migrate       - (Requires db-up) Apply all Alembic migrations to 'head'."
	@echo "  migrate-new M=\"...\" - (Requires db-up) Create a new auto-generated migration."


# ==============================================================================
# Project & Dependencies
# ==============================================================================

install:
	@echo "Installing dependencies..."
	@poetry install

clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -exec rm -r {} +
	@find . -type d -name ".ruff_cache" -exec rm -r {} +


# ==============================================================================
# Local Development
# ==============================================================================

run: db-up
	@$(VENV_RUN) uvicorn $(APP_MODULE) --host 127.0.0.1 --port 8000 --reload

test:
	@$(VENV_RUN) pytest $(TEST_DIR) -s

format:
	@echo "Formatting code..."
	@$(VENV_RUN) black $(SRC_DIR) $(TEST_DIR)

lint:
	@echo "Linting code..."
	@$(VENV_RUN) ruff check $(SRC_DIR) $(TEST_DIR)

check: lint
	@echo "Checking code formatting..."
	@$(VENV_RUN) black --check $(SRC_DIR) $(TEST_DIR)


# ==============================================================================
# Docker Services (Database)
# ==============================================================================

db-up:
	@docker compose up -d $(DB_SERVICE)

db-down:
	@docker compose down

db-logs:
	@docker compose logs -f $(DB_SERVICE)

# ==============================================================================
# Migrations (Alembic)
# ==============================================================================
migrate: db-up
	@cd $(MIGRATIONS_DIR) && $(VENV_RUN) alembic upgrade head

migrate-new: db-up
	@cd $(MIGRATIONS_DIR) && $(VENV_RUN) alembic revision --autogenerate -m "$(M)"
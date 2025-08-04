.PHONY: help install install-dev lint format test test-cov clean setup-dev run-web run-recorder

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	uv pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

setup-dev: install-dev ## Setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make lint' to check code quality"
	@echo "Run 'make test' to run tests"

lint: ## Run linting checks
	ruff check .
	mypy .

format: ## Format code
	ruff format .
	ruff check --fix .

test: ## Run tests
	pytest -v

test-cov: ## Run tests with coverage
	pytest --cov=. --cov-report=html --cov-report=term-missing

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/

run-web: ## Run the web application
	cd web-app && streamlit run main.py

run-recorder: ## Run the desktop recorder
	cd desktop-recorder && python main.py

# Docker commands (if needed)
docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start all services
	docker-compose up -d

docker-down: ## Stop all services
	docker-compose down

docker-logs: ## View logs
	docker-compose logs -f 
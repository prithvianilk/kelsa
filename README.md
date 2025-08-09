# Kelsa

**Track and analyze your work and time**

> My computer tells me what I'm doing → Kafka → Pinot → pretty charts that make me feel bad about my productivity

Kelsa is a comprehensive work tracking and analytics platform that captures desktop activity, processes it through a real-time data pipeline, and provides insightful visualizations of your productivity patterns.

Pleae make sure you have uv installed, we use uv for our package management and ruff for linting.

## Architecture

- **Desktop Recorder**: Captures application usage and activity
- **Kafka**: Streams activity data in real-time
- **Apache Pinot**: Stores and processes time-series analytics data
- **Web App**: Streamlit-based dashboard with FastAPI backend

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for Pinot/Kafka)

### Development Setup

1. **Clone and setup the project:**

   ```bash
   git clone <repository-url>
   cd kelsa
   make setup-dev
   ```

2. **Configure environment:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start infrastructure:**

   ```bash
   make docker-up
   ```

4. **Run the applications:**

   ```bash
   # Terminal 1: Web app
   make run-web

   # Terminal 2: Desktop recorder
   make run-recorder
   ```

### Production Setup

1. **Install dependencies:**

   ```bash
   make install
   ```

2. **Configure environment variables** (see `.env.example`)

3. **Start services:**
   ```bash
   make docker-up
   python web-app/main.py
   python desktop-recorder/main.py
   ```

## Configuration

### Desktop Recorder

Create `config.env` in the project root or configure via environment variables:

- **`API_URL`**: Web app endpoint (e.g., `http://localhost:8000`)
- **`USERNAME`**: Authentication username
- **`PASSWORD`**: Authentication password


### Web App

Create `config.env` in the project root or configure via environment variables:

- **`HTPASSWD_FILE`**: The path to the htpasswd file (e.g., `~/users/me/kelsa/pinot/data/nginx/.htpasswd`)

## Development

### Available Commands

```bash
make help              # Show all available commands
make setup-dev         # Setup development environment
make lint             # Run linting checks
make format           # Format code with ruff
make test             # Run tests
make test-cov         # Run tests with coverage
make clean            # Clean temporary files
```

### Code Quality

The project uses:

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks for quality checks

### Project Structure

```
kelsa/
├── common/              # Shared utilities
├── desktop-recorder/    # Activity capture service
├── web-app/            # Streamlit dashboard + FastAPI
├── pinot/              # Database schemas and config
└── pyproject.toml      # Project configuration
```

## Usage

1. **Start the infrastructure** (Kafka + Pinot):

   ```bash
   make docker-up
   ```

2. **Launch the web dashboard**:

   ```bash
   make run-web
   ```

   Visit: http://localhost:8501

3. **Start activity tracking**:
   ```bash
   make run-recorder
   ```

## Contributing

1. Setup development environment: `make setup-dev`
2. Make your changes
3. Run quality checks: `make lint format test`
4. Submit a pull request

## License

[Add your license here]

# Web Application Docker Setup

This directory contains the Docker configuration for the web application components.

## Components

- **Streamlit App** (`main.py`): Web dashboard for work tracking visualization
- **FastAPI App** (`api.py`): REST API for work data ingestion

## Dockerfile

The `Dockerfile` is configured to run either the Streamlit or FastAPI application based on the command passed to the container.

## Usage

### Building the Image

```bash
docker build -t web-app .
```

### Running Individual Services

#### Streamlit App (Port 8501)
```bash
docker run -p 8501:8501 web-app streamlit
```

#### FastAPI App (Port 8000)
```bash
docker run -p 8000:8000 web-app api
```

### Using Docker Compose

The web application services are integrated into the main docker-compose files:

- `../pinot/docker-compose.yaml` (Development)
- `../pinot/docker-compose.prod.yaml` (Production)

#### Start all services:
```bash
cd ../pinot
docker-compose up -d
```

#### Start only web services:
```bash
cd ../pinot
docker-compose up web-app-streamlit web-app-api
```

## Services

### web-app-streamlit
- **Port**: 8501
- **Purpose**: Streamlit dashboard for work tracking visualization
- **Dependencies**: Pinot Broker (for data access)

### web-app-api
- **Port**: 8000
- **Purpose**: FastAPI REST API for work data ingestion
- **Dependencies**: Kafka (for data streaming)

## Environment Variables

- `PYTHONPATH`: Set to include both the app directory and common module
- Additional environment variables can be configured in the docker-compose files

## Health Checks

- Streamlit: `http://localhost:8501/_stcore/health`
- FastAPI: `http://localhost:8000/docs`

## Volumes

The services mount the following volumes for development:
- Web app source code
- Common module for shared functionality

## Network

Both services are connected to the `pinot-demo` network to communicate with Pinot and Kafka services.
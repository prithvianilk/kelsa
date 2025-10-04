#! /usr/bin/env python3

import os
import sys

from fastapi import FastAPI, HTTPException, Request, Query
from kafka import KafkaProducer
from services.user_service import HtpasswdUserService
from services.work_ingestion_service import KafkaWorkIngestionService
from services.main_page_service import MainPageService
from services.by_app_service import ByAppService
from work_repo import PinotWorkRepo
from pinot_conn import conn
import uvicorn
from work import Work
from dtos.main_page import MainPageData
from dtos.by_app import ByAppData
from middlewares.cors import add_cors_middleware
from services.worker.report_generation_worker import ReportGenerationWorker
from flink.data_stream_factory import FlinkDataStreamFactory

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.auth import decode_auth_header
from common.config import DotEnvEnvironmentVariables
from common.logger import LogLevel, get_customised_logger

KAFKA_BOOTSTRAP_SERVERS = "localhost:9094"
KAFKA_TOPIC = "work-topic"

logger = get_customised_logger(LogLevel.INFO)
config = DotEnvEnvironmentVariables("config.env")

app = FastAPI(title="Kelsa Work API", description="API for work tracking data")

kafka_producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS])
work_ingestion_service = KafkaWorkIngestionService(logger, kafka_producer, KAFKA_TOPIC)
user_service = HtpasswdUserService(config.get_config("HTPASSWD_FILE"))

data_stream_factory = FlinkDataStreamFactory(
    KAFKA_BOOTSTRAP_SERVERS, 
    KAFKA_TOPIC, 
    config.get_config("FLINK_SQL_CONNECTOR_KAFKA_JAR"))
report_generation_worker = ReportGenerationWorker(
    data_stream_factory, 
    config.get_config("STREAM_OUTPUT_LOGS_DIR"))

# TODO
# - Add a health check endpoint

add_cors_middleware(app)

@app.middleware("http")
async def auth(request: Request, call_next):
    if config.get_config("ADMIN_MODE") == "true":
        request.state.username = "admin"
        return await call_next(request)

    if request.method == "OPTIONS":
        return await call_next(request)

    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    try:
        username, password = decode_auth_header(auth_header)
        if not user_service.verify_credentials(username, password):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        request.state.username = username

    except (ValueError, IndexError, UnicodeDecodeError):
        logger.error(f"Invalid authorization header format: {auth_header}")
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    response = await call_next(request)
    return response


@app.post("/api/work")
async def record_work(request: Request, work: Work):
    """Record work"""
    authenticated_username = request.state.username

    if work.username != authenticated_username:
        logger.debug(f"Work username does not match authenticated user: {work.username} != {authenticated_username}")
        raise HTTPException(
            status_code=403, detail="Work username does not match authenticated user"
        )

    logger.info(f"Received work: {work}")
    work_ingestion_service.ingest_work(work)


@app.get("/api/v1/main-page-data")
async def get_main_page_data(
    request: Request,
    since_time: int = Query(..., description="Start time filter in epoch milliseconds"),
    till_time: int = Query(None, description="End time filter in epoch milliseconds"),
    only_active_work: bool = Query(False, description="Filter for active work only")
) -> MainPageData:
    """Get main page data"""
    username = request.state.username
    main_page_service = get_main_page_service(username)
    
    till_time = handle_none_till_time(till_time)
    
    try:
        return main_page_service.get_main_page_data(since_time, till_time, only_active_work)
    except Exception as e:
        logger.error(f"Error getting main page data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving main page data")


@app.get("/api/v1/by-app-data")
async def get_by_app_data(
    request: Request,
    app: str = Query(..., description="Application name"),
    since_time: int = Query(..., description="Start time filter in epoch milliseconds"),
    till_time: int = Query(None, description="End time filter in epoch milliseconds"),
    only_active_work: bool = Query(False, description="Filter for active work only")
) -> ByAppData:
    """Get by-app data with grouped work information"""
    username = request.state.username
    by_app_service = get_by_app_service(username)
    
    till_time = handle_none_till_time(till_time)
    
    try:
        return by_app_service.get_by_app_data(since_time, till_time, app, only_active_work)
    except Exception as e:
        logger.error(f"Error getting by-app data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving by-app data")


def get_main_page_service(username: str) -> MainPageService:
    return MainPageService(logger, PinotWorkRepo(conn, logger, username))


def get_by_app_service(username: str) -> ByAppService:
    return ByAppService(logger, PinotWorkRepo(conn, logger, username))

def handle_none_till_time(till_time: int | None) -> int:
    if till_time is None:
        return get_default_till_time()
    return till_time

def get_default_till_time() -> int:
    import time
    return int(time.time() * 1000)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

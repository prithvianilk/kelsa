#! /usr/bin/env python3

import uvicorn
import base64
from fastapi import FastAPI, Request, HTTPException
from kafka import KafkaProducer
from work import Work
from services.work_ingestion_service import KafkaWorkIngestionService
from services.user_service import HtpasswdUserService

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_customised_logger, LogLevel
from common.config import DotEnvEnvironmentVariables
from common.auth import decode_auth_header
logger = get_customised_logger(LogLevel.INFO)
config = DotEnvEnvironmentVariables("config.env")

app = FastAPI(title="Kelsa Work API", description="API for work tracking data")
kafka_producer = KafkaProducer(bootstrap_servers=['localhost:9094'])
work_ingestion_service = KafkaWorkIngestionService(logger, kafka_producer, 'work-topic')
user_service = HtpasswdUserService(config.get_config("HTPASSWD_FILE"))

# TODO
# - Add a health check endpoint

@app.middleware("http")
async def auth(request: Request, call_next):
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
        raise HTTPException(status_code=403, detail="Work username does not match authenticated user")
    
    logger.info(f"Received work: {work}")
    work_ingestion_service.ingest_work(work)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 

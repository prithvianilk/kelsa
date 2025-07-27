#! /usr/bin/env python3

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from kafka import KafkaProducer
from work import Work
from services.work_ingestion_service import KafkaWorkIngestionService

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_customised_logger, LogLevel
from common.config import DotEnvEnvironmentVariables
logger = get_customised_logger(LogLevel.INFO)
config = DotEnvEnvironmentVariables("config.env")

app = FastAPI(title="Kelsa Work API", description="API for work tracking data")
kafka_producer = KafkaProducer(bootstrap_servers=['localhost:9094'])
work_ingestion_service = KafkaWorkIngestionService(logger, kafka_producer, 'work-topic')

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.middleware("http")
async def auth(request: Request, call_next):
    api_token = request.headers.get("x-api-token")
    if api_token != config.get_config("API_TOKEN"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    response = await call_next(request)
    return response

@app.post("/api/work")
async def record_work(work: Work):
    """Record work"""
    logger.info(f"Received work: {work}")
    work_ingestion_service.ingest_work(work)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
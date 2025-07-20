from abc import abstractmethod
from kafka import KafkaProducer
from work import Work

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.logger import Logger

class WorkIngestionService:
    def __init__(self, logger: Logger):
        self.logger = logger
        pass

    @abstractmethod
    def ingest_work(self, work: Work):
        pass

class KafkaWorkIngestionService(WorkIngestionService):
    def __init__(self, logger: Logger, kafka_producer: KafkaProducer, topic_name: str):
        super().__init__(logger)
        self.kafka_producer = kafka_producer
        self.topic_name = topic_name

    def ingest_work(self, work: Work):
        work_json = work.model_dump_json().encode('utf-8')
        self.logger.info(f"Ingesting to topic: {self.topic_name}, work: {work_json}")
        self.kafka_producer.send(self.topic_name, work_json)
        self.kafka_producer.flush()
        self.logger.info("Work ingested successfully")
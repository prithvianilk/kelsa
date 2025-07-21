from abc import abstractmethod
import time
import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import Logger
from application_details_fetcher import ApplicationDetailsFetcher

class WorkRecorder:
    def __init__(self, logger: Logger):
        self.logger = logger

    def build_work(self, app, tab, is_active):
        return {
            "application": app,
            "tab": tab,
            "active": is_active,
            "done_at": int(time.time() * 1000)
        }

    @abstractmethod
    def record_work(self):
        pass

    @abstractmethod
    def publish_work(self, work: dict):
        pass

class SingleFetcherWorkRecorder(WorkRecorder):
    def __init__(self, logger: Logger, fetcher: ApplicationDetailsFetcher):
        super().__init__(logger)
        self.fetcher = fetcher
    
    def record_work(self):
        app, tab, is_active = self.fetcher.get_active_application_details()
        work = self.build_work(app, tab, is_active)
        self.publish_work(work)
        self.logger.info(f"Recorded work: {work}")

class KafkaWorkRecorder(SingleFetcherWorkRecorder):
    def __init__(self, logger: Logger, fetcher: ApplicationDetailsFetcher, kafka_producer, topic_name):
        super().__init__(logger, fetcher)
        self.kafka_producer = kafka_producer
        self.topic_name = topic_name

    def publish_work(self, work: dict):
        self.kafka_producer.send(self.topic_name, value=work)
        self.kafka_producer.flush()
        self.logger.info(f"Published work to Kafka: {work}")

class ApiWorkRecorder(SingleFetcherWorkRecorder):
    def __init__(self, logger: Logger, fetcher: ApplicationDetailsFetcher, base_url: str):
        super().__init__(logger, fetcher)
        self.base_url = base_url.rstrip('/')

    def publish_work(self, work: dict):
        try:
            response = requests.post(
                f"{self.base_url}/api/work",
                json=work,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            self.logger.info(f"Successfully published work to API: {work}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to publish work to API: {e}")
            raise
from abc import abstractmethod
import os
import sys
import time

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from application_details_fetcher import ApplicationDetailsFetcher

from common.auth import encode_auth_header
from common.logger import Logger


class WorkRecorder:
    def __init__(self, logger: Logger, username: str, password: str):
        self.logger = logger
        self.username = username
        self.password = password

    def build_work(self, app, tab, is_active):
        return {
            "application": app,
            "tab": tab,
            "active": is_active,
            "done_at": int(time.time() * 1000),
            "username": self.username,
        }

    @abstractmethod
    def record_work(self):
        pass

    @abstractmethod
    def publish_work(self, work: dict):
        pass


class SingleFetcherWorkRecorder(WorkRecorder):
    def __init__(
        self, logger: Logger, fetcher: ApplicationDetailsFetcher, username: str, password: str
    ):
        super().__init__(logger, username, password)
        self.fetcher = fetcher

    def record_work(self):
        app, tab, is_active = self.fetcher.get_active_application_details()
        if app is None:
            self.logger.error("No application details found, skipping work recording")
            return

        work = self.build_work(app, tab, is_active)
        self.publish_work(work)
        self.logger.info(f"Recorded work: {work}")


class KafkaWorkRecorder(SingleFetcherWorkRecorder):
    def __init__(
        self,
        logger: Logger,
        fetcher: ApplicationDetailsFetcher,
        kafka_producer,
        topic_name,
        username,
        password,
    ):
        super().__init__(logger, fetcher, username, password)
        self.kafka_producer = kafka_producer
        self.topic_name = topic_name

    def publish_work(self, work: dict):
        self.kafka_producer.send(self.topic_name, value=work)
        self.kafka_producer.flush()
        self.logger.info(f"Published work to Kafka: {work}")


class ApiWorkRecorder(SingleFetcherWorkRecorder):
    def __init__(
        self,
        logger: Logger,
        fetcher: ApplicationDetailsFetcher,
        base_url: str,
        username: str,
        password: str,
    ):
        super().__init__(logger, fetcher, username, password)
        self.base_url = base_url.rstrip("/")

    def publish_work(self, work: dict):
        try:
            auth_header = encode_auth_header(self.username, self.password)

            headers = {"Content-Type": "application/json", "Authorization": auth_header}

            response = requests.post(
                f"{self.base_url}/api/work", json=work, headers=headers, timeout=10
            )
            response.raise_for_status()
            self.logger.info(f"Successfully published work to API: {work}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to publish work to API: {e}")
            pass

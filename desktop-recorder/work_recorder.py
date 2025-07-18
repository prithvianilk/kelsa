from abc import abstractmethod
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import Logger

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
    def __init__(self, fetcher, logger: Logger):
        super().__init__(logger)
        self.fetcher = fetcher
    
    def record_work(self):
        app, tab, is_active = self.fetcher.get_active_application_details()
        work = self.build_work(app, tab, is_active)
        self.publish_work(work)
        self.logger.info(f"Recorded work: {work}")

class FirstSuccessfulFetcherWorkRecorder(WorkRecorder):
    def __init__(self, fetchers, logger: Logger, work_recorder):
        super().__init__(logger)
        self.fetchers = fetchers
        self.work_recorder = work_recorder

    def record_work(self):
        for index, fetcher in enumerate(self.fetchers):
            app, tab, is_active = fetcher.get_active_application_details()
            self.logger.info(f"Fetcher {index} found work: {app} {tab}")
            if app is not None and tab is not None and tab != "":
                work = self.build_work(app, tab, is_active)
                self.publish_work(work)
                return

    def publish_work(self, work: dict):
        self.work_recorder.publish_work(work)

class KafkaWorkRecorder(SingleFetcherWorkRecorder):
    def __init__(self, fetcher, logger: Logger, kafka_producer, topic_name):
        super().__init__(fetcher, logger)
        self.kafka_producer = kafka_producer
        self.topic_name = topic_name

    def publish_work(self, work: dict):
        self.kafka_producer.send(self.topic_name, value=work)
        self.kafka_producer.flush()
        self.logger.info(f"Published work to Kafka: {work}")
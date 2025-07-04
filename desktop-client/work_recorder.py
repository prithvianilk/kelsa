from abc import abstractmethod
import time

class WorkRecorder:
    def __init__(self, fetcher, logger):
        self.fetcher = fetcher
        self.logger = logger

    def record_work(self):
        app, tab = self.fetcher.get_active_application_details()

        work = {
            "application": app,
            "tab": tab,
            "done_at": int(time.time() * 1000)
        }

        self.publish_work(work)
        self.logger.log(f"Recorded work: {work}")

    @abstractmethod
    def publish_work(self, work: dict):
        pass

class KafkaWorkRecorder(WorkRecorder):
    def __init__(self, fetcher, logger, kafka_producer, topic_name):
        super().__init__(fetcher, logger)
        self.kafka_producer = kafka_producer
        self.topic_name = topic_name

    def publish_work(self, work: dict):
        self.kafka_producer.send(self.topic_name, value=work)
        self.kafka_producer.flush()
        self.logger.log(f"Published work to Kafka: {work}")
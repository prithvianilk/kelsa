import json
from kafka import KafkaProducer
import time
from application_details_fetcher import JxaApplicationDetailsFetcher
from work_recorder import KafkaWorkRecorder
from logger import ConsoleLogger

producer = KafkaProducer(
    bootstrap_servers=['localhost:9094'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
fetcher = JxaApplicationDetailsFetcher()
logger = ConsoleLogger()
recorder = KafkaWorkRecorder(fetcher, logger, producer, 'work-topic')

while True:
    recorder.record_work()
    time.sleep(1)
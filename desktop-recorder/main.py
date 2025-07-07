import json
from kafka import KafkaProducer
import time
from application_details_fetcher import JxaApplicationDetailsFetcher, AppleScriptApplicationDetailsFetcher
from work_recorder import KafkaWorkRecorder, FirstSuccessfulWorkRecorder
from logger import ConsoleLogger

producer = KafkaProducer(
    bootstrap_servers=['localhost:9094'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
fetchers = [JxaApplicationDetailsFetcher(), AppleScriptApplicationDetailsFetcher()]
logger = ConsoleLogger()
recorder = FirstSuccessfulWorkRecorder(fetchers, logger, KafkaWorkRecorder(fetchers, logger, producer, 'work-topic'))

while True:
    recorder.record_work()
    time.sleep(1)
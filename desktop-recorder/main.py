import json
import os
import sys
from kafka import KafkaProducer
import time
from application_details_fetcher import JxaApplicationDetailsFetcher, AppleScriptApplicationDetailsFetcher
from work_recorder import KafkaWorkRecorder, FirstSuccessfulFetcherWorkRecorder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import ConsoleLogger

producer = KafkaProducer(
    bootstrap_servers=['localhost:9094'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
fetchers = [JxaApplicationDetailsFetcher(), AppleScriptApplicationDetailsFetcher()]
logger = ConsoleLogger()
recorder = FirstSuccessfulFetcherWorkRecorder(fetchers, logger, KafkaWorkRecorder(None, logger, producer, 'work-topic'))

while True:
    recorder.record_work()
    time.sleep(1)
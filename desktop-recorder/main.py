import os
import sys
import time
from application_details_fetcher import JxaApplicationDetailsFetcher, AppleScriptApplicationDetailsFetcher
from work_recorder import FirstSuccessfulFetcherWorkRecorder, ApiWorkRecorder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_customised_logger, LogLevel
logger = get_customised_logger(LogLevel.INFO)

fetchers = [JxaApplicationDetailsFetcher(), AppleScriptApplicationDetailsFetcher()]
recorder = FirstSuccessfulFetcherWorkRecorder(fetchers, logger, ApiWorkRecorder(None, 'http://localhost:8000', logger))

while True:
    recorder.record_work()
    time.sleep(1)
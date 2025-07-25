#! /usr/bin/env python3

import os
import sys
import time
from application_details_fetcher import FirstSuccessfulApplicationDetailsFetcher, JxaApplicationDetailsFetcher, AppleScriptApplicationDetailsFetcher
from work_recorder import ApiWorkRecorder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_customised_logger, LogLevel
from common.config import DotEnvEnvironmentVariables
logger = get_customised_logger(LogLevel.INFO)
config = DotEnvEnvironmentVariables("config.env")

fetcher = FirstSuccessfulApplicationDetailsFetcher(logger, [JxaApplicationDetailsFetcher(), AppleScriptApplicationDetailsFetcher()])
recorder = ApiWorkRecorder(logger, fetcher, config.get_config("API_URL"), config.get_config("API_TOKEN"))

while True:
    recorder.record_work()
    time.sleep(1)
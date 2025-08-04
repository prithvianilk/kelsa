#! /usr/bin/env python3

import os
import sys
import time

from application_details_fetcher import (
    AppleScriptApplicationDetailsFetcher,
    FirstSuccessfulApplicationDetailsFetcher,
    JxaApplicationDetailsFetcher,
)
from work_recorder import ApiWorkRecorder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.config import DotEnvEnvironmentVariables
from common.logger import LogLevel, get_customised_logger

logger = get_customised_logger(LogLevel.INFO)
config = DotEnvEnvironmentVariables("config.env")

fetcher = FirstSuccessfulApplicationDetailsFetcher(
    logger, [JxaApplicationDetailsFetcher(), AppleScriptApplicationDetailsFetcher()]
)
recorder = ApiWorkRecorder(
    logger,
    fetcher,
    config.get_config("API_URL"),
    config.get_config("USERNAME"),
    config.get_config("PASSWORD"),
)

while True:
    recorder.record_work()
    time.sleep(1)

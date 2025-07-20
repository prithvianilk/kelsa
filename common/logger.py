from abc import abstractmethod
from enum import Enum

class Logger:
    def __init__(self):
        pass

    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def debug(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass

class LogLevel(Enum):
    INFO = 0
    DEBUG = 1
    ERROR = 2

    def __ge__(self, other):
        return self.value >= other.value

class LevelAndAboveLogger(Logger):
    def __init__(self, logger: Logger, level: LogLevel):
        self.logger = logger
        self.level = level

    def info(self, message):
        if self.level >= LogLevel.INFO:
            self.logger.info(message)

    def debug(self, message):
        if self.level >= LogLevel.DEBUG:
            self.logger.debug(message)

    def error(self, message):
        if self.level >= LogLevel.ERROR:
            self.logger.error(message)

class ConsoleLogger(Logger):
    def info(self, message):
        print(message)

    def debug(self, message):
        print(message)

    def error(self, message):
        print(message)

class LevelPrefixedLogger(Logger):
    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger

    def info(self, message):
        self.logger.info(f"INFO:     {message}")

    def debug(self, message):
        self.logger.debug(f"DEBUG:     {message}")
    
    def error(self, message):
        self.logger.error(f"ERROR:     {message}")

class NoopLogger(Logger):
    def info(self, message):
        pass

    def debug(self, message):
        pass

    def error(self, message):
        pass

def get_customised_logger(level: LogLevel):
    return LevelAndAboveLogger(LevelPrefixedLogger(ConsoleLogger()), level)
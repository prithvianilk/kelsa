from abc import abstractmethod

class Logger:
    def __init__(self):
        pass

    @abstractmethod
    def log(self, message):
        pass

class ConsoleLogger(Logger):
    def log(self, message):
        print(message)

class NoopLogger(Logger):
    def log(self, message):
        pass
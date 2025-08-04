from abc import abstractmethod

from dotenv import dotenv_values


class Config:
    @abstractmethod
    def get_config(self, key: str):
        pass


class DotEnvEnvironmentVariables(Config):
    def __init__(self, path: str):
        self.path = path
        self.values = dotenv_values(self.path)

    def get_config(self, key: str):
        return self.values[key]

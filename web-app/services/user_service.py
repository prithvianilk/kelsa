from abc import abstractmethod
from passlib.apache import HtpasswdFile
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_customised_logger, LogLevel
logger = get_customised_logger(LogLevel.INFO)

class UserService:
    def __init__(self):
        pass

    @abstractmethod
    def verify_credentials(self, username: str, password: str):
        pass

class HtpasswdUserService(UserService):
    def __init__(self, path: str):
        self.path = path

    def verify_credentials(self, username: str, password: str):
        """Verify username/password against htpasswd file"""
        try:
            # Use passlib to load and verify htpasswd file
            htpasswd = HtpasswdFile(self.path)
            return htpasswd.check_password(username, password)
        except FileNotFoundError:
            logger.error(f"htpasswd file not found: {self.path}")
            return False
        except Exception as e:
            logger.error(f"Error verifying credentials: {e}")
            return False